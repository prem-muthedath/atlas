#!/usr/bin/python

from .schema import _Schema
from database import _AtlasDB

from collections import OrderedDict
from aenum import Enum, NoAlias

################################################################################

class _Report(object):
    def __init__(self):
        self.__contents=[]

    def _render(self, bom, schema):
        part_maps=_AtlasDB()._part_maps()
        for index, cost_map in enumerate(bom._cost_maps()):
            part_map=part_maps[index]
            part_map.update(cost_map)
            line=OrderedDict([(i, part_map[i]) for i in schema])
            self.__contents=[line] if index==0 else self.__contents + [line]
        return self._empty() if self.__is_empty() else self._render_()

    def __is_empty(self):
        return any([i==[] for i in [self.__contents, self._names()]])

    def _empty(self):
        pass

    def _render_(self):
        pass

    def _body(self):
        return [(i+1, self.__format(j)) for i, j in enumerate(self.__contents)]

    def __format(self, line):
        items=OrderedDict()
        for (col, val) in line.items():
            val=str(val)
            items[col]=('$' + val) if col in _Schema._costs_schema() else val
        return items

    def _names(self):
        return self.__contents[0].keys() if len(self.__contents) > 0 else []

    def _totals(self):
        totals=OrderedDict()
        columns=[i for i in _Schema._totals_schema() if i in self._names()]
        for col in columns:
            totals[col]=col._total([line[col] for line in self.__contents])
        return self.__format(totals)

################################################################################

class _TextReport(_Report):
    def _empty(self):
        return _TextView([])._render()

    def _render_(self):
        contents=[self.__header()] + self.__body() + [self.__footer()]
        return _TextView(contents)._render()

    def __header(self):
        cells=['item'] + [i.name for i in self._names()]
        return _BorderedRow([self.__capitalize(i) for i in cells])

    def __capitalize(self, word):
        return ' '.join(each[:1].upper()+each[1:].lower() \
                for each in word.split('_'))

    def __body(self):
        return [self.__row(i, row) for (i, row) in self._body()]

    def __row(self, index, row):
        if row.has_key(_Schema.level):
            level=row[_Schema.level]
            indent=(int(level))*"  "
            row[_Schema.level]=indent+level
        return _TextRow([str(index)] + row.values())

    def __footer(self):
        totals=self._totals()
        cells=(['totals'] if len(totals) > 0 else ['']) + self.__totals(totals)
        return _BorderedRow([self.__capitalize(i) for i in cells])

    def __totals(self, totals):
        return [totals[i] if totals.has_key(i) else '' for i in self._names()]

################################################################################

class _TextRow(object):
    def __init__(self, cells):
        self.__cells=cells
        self.__field_width=20
        self.__sep='|'

    def _render(self):
        data=self.__sep.join([self.__centered(i) for i in self.__cells])
        return self.__sep.join(['', data, ''])

    def __centered(self, value):
        return value.center(self.__field_width)

    def _is_empty(self):
        return all([i=='' for i in self.__cells])

    def _width(self):
        return len(self.__cells)*self.__field_width + self.__sep_width()

    def __sep_width(self):
        sep_count=len(self.__cells) + 1
        return sep_count*len(self.__sep)


class _BorderedRow(_TextRow):
    def __init__(self, cells):
        super(_BorderedRow, self).__init__(cells)
        self.__symbol='-'

    def _render(self):
        if self._is_empty():
            return [self.__border()]
        return [self.__border(), super(_BorderedRow, self)._render(), self.__border()]

    def __border(self):
        return self.__symbol * self._width()

################################################################################

class _TextView:
    def __init__(self, contents):
        self.__contents=contents

    def _render(self):
        data=[]
        for i in self.__contents:
            if isinstance(i, _BorderedRow):
                data.extend(i._render())
            else:
                data.append(i._render())
        return self.__sep().join(data)

    def __sep(self):
        return '\n' if len(self.__contents) > 0 else ''

################################################################################

class _XmlReport(_Report):
    def _empty(self):
        return _XmlTree(_Xsd.tag.value, [])._render()

    def _render_(self):
        return self.__process(_Xsd)._render()

    def __process(self, item, data=None):
        vals=item.nodes.value
        if item == _Xsd:
            result=[self.__process(i) for i in vals]
            return _XmlTree(item.tag.value, [i for i in result if i !=None])
        if item == _Parts:
            result=[self.__process(vals[0], i) for (_, i) in self._body()]
            return _XmlTree(item.tag.value, result)
        if item == _Part:
            return _XmlTree(item.tag.value, self.__nodes(data))
        if item == _Totals:
            totals=self._totals()
            if len(totals) > 0:
                return _XmlTree(item.tag.value, self.__nodes(totals))
            return None
        raise RuntimeError('element ' + str(item) + ' missing handler.')

    def __nodes(self, row):
        return [_XmlNode(i.name, j) for (i, j) in row.items()]

################################################################################

class _Part(Enum):
    tag='part'
    nodes=[_Schema]

class _Totals(Enum):
    tag='totals'
    nodes=_Schema._totals_schema()

class _Parts(Enum):
    tag='parts'
    nodes=[_Part]

class _Xsd(Enum):
    tag='xml'
    nodes=[_Parts, _Totals]

################################################################################

class _Xml(object):
    def __init__(self, tag):
        self.__tag=tag

    def _render(self):
        pass

    def _element(self, value):
        return '<' + self.__tag + '>' + value + '</' + self.__tag + '>'


class _XmlTree(_Xml):
    def __init__(self, tag, children):
        super(_XmlTree, self).__init__(tag)
        self.__children=children

    def _render(self):
        sep='\n' if len(self.__children) > 0 else ''
        value=sep + sep.join([i._render() for i in self.__children]) + sep
        return self._element(value)


class _XmlNode(_Xml):
    def __init__(self, tag, value):
        super(_XmlNode, self).__init__(tag)
        self.__value=value

    def _render(self):
        return self._element(str(self.__value))

################################################################################

