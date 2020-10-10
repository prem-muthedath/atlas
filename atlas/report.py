#!/usr/bin/python

from .schema import _Schema
from database import _AtlasDB

from collections import OrderedDict

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
            if col in [_Schema.unit_cost, _Schema.cost]:
                val='$' + val
            items[col]=val
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
        return ""

    def _render_(self):
        contents=[self.__header()] + self.__body() + [self.__footer()]
        return _TextView(contents)._render()

    def __header(self):
        cells=['items'] + [i.name for i in self._names()]
        return _BorderedRow([self.__capitalize(i) for i in cells])

    def __capitalize(self, word):
        return ' '.join(each[:1].upper()+each[1:].lower() \
                for each in word.split('_'))

    def __body(self):
        results=[self.__row(i, row) for (i, row) in self._body()]
        return [_TextRow(i) for i in results]

    def __row(self, index, row):
        return [str(index)] + \
            [self.__level(j) if i==_Schema.level else j for (i, j) in row.items()]

    def __level(self, level):
        indent=(int(level))*"  "
        return indent+level

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
        return self.__cells==[] or all([i=='' for i in self.__cells])

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
        self.__sep='\n'

    def _render(self):
        data=[]
        for i in self.__contents:
            if isinstance(i, _BorderedRow):
                data.extend(i._render())
            else:
                data.append(i._render())
        return self.__sep.join(data)

################################################################################

class _XmlReport(_Report):
    def __init__(self):
        super(_XmlReport, self).__init__()
        self.__tags={
                "XML" : "xml",
                "PARTS" : "parts",
                "PART" : "part",
                "TOTALS" : "totals"
            }

    def _empty(self):
        return self.__element(self.__tags["XML"], "")

    def __element(self, name, value):
        return '<' + name + '>' + value.__str__() + '</' + name + '>'

    def _render_(self):
        elems=_XmlElements([i for i in self.__contents()])
        return self.__element(self.__tags["XML"], elems)

    def __contents(self):
        totals=self._totals()
        if len(totals) > 0:
            return [self.__body(), self.__footer(totals)]
        return [self.__body()]

    def __body(self):
        return self.__element(self.__tags["PARTS"], _XmlElements(self.__parts()))

    def __parts(self):
        parts=[]
        for (_, line) in self._body():
            part=self.__xml(self.__tags['PART'], line.items())
            parts.append(part)
        return parts

    def __xml(self, tag, items):
        elems=_XmlElements([self.__element(i.name, j) for (i, j) in items])
        return self.__element(tag, elems)

    def __footer(self, totals):
        return self.__xml(self.__tags['TOTALS'], totals.items())

################################################################################

class _XmlElements:
    def __init__(self, elems):
        self.__elems=elems
        self.__sep='\n'

    def __str__(self):
        return self.__sep.join(["", self.__data(), ""])

    def __data(self):
        return self.__sep.join(self.__elems)

################################################################################

