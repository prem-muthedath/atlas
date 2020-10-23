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
        sections=self.__header() + self.__body() + self.__footer()
        return _TextView(sections)._render()

    def __header(self):
        title='Atlas Bill of Materials Report'
        cols=['Item'] + [self.__capitalize(i.name) for i in self._names()]
        return self.__sections([(_Title, title), (_Data, [cols])])

    def __capitalize(self, word):
        return ' '.join(each[:1].upper()+each[1:].lower() \
                for each in word.split('_'))

    def __sections(self, sections):
        size=len(self._names()) + 1
        return [i._new(size, j) for (i, j) in sections]

    def __body(self):
        data=[self.__row(i, row) for (i, row) in self._body()]
        return self.__sections([(_Data, data)])

    def __row(self, index, row):
        if row.has_key(_Schema.level):
            level=row[_Schema.level]
            indent=(int(level))*"  "
            row[_Schema.level]=indent+level
        return [str(index)] + row.values()

    def __footer(self):
        totals=self._totals()
        if len(totals) == 0: return []
        return self.__sections([self.__totals(totals), self.__note()])

    def __totals(self, totals):
        caption=['Totals']
        data=[totals[i] if totals.has_key(i) else '' for i in self._names()]
        return (_Data, [caption + data])

    def __note(self):
        note="Note: Totals computed only for 'Quantity', 'Costed', 'Cost'."
        return (_Note, note)

################################################################################

class _TextView(object):
    def __init__(self, sections):
        self.__sections=sections

    def _render(self):
        if len(self.__sections)==0: return ''
        result=[]
        for section in self.__sections:
            section._render(result)
        return '\n'.join(result)

################################################################################

class _TextGrid(object):
    def __init__(self, size):
        self.__size=size
        self.__field_width=20
        self.__sep='|'

    def _render(self):
        pass

    def _row(self, cells):
        data=self.__sep.join([self.__centered(i) for i in cells])
        return self.__sep.join(['', data, ''])

    def __centered(self, value):
        return value.center(self.__field_width)

    def _border(self):
        return '-' * self.__width()

    def __width(self):
        return self.__size*self.__field_width + self.__sep_width()

    def __sep_width(self):
        sep_count=self.__size + 1
        return sep_count*len(self.__sep)


class _TextRow(_TextGrid):
    def __init__(self, cells):
        super(_TextRow, self).__init__(len(cells))
        self.__cells=cells

    def _render(self):
        return self._row(self.__cells)

################################################################################

class _TextSection(object):
    def __init__(self, grid):
        self.__grid=grid

    def _render(self, result):
        pass

    def _border(self):
        return self.__grid._border()


class _Data(_TextSection):
    def __init__(self, grid, rows):
        super(_Data, self).__init__(grid)
        self.__rows=rows

    @classmethod
    def _new(cls, size, rows):
        return _Data(_TextGrid(size), [_TextRow(i) for i in rows])

    def _render(self, result):
        for row in self.__rows:
            result.append(row._render())
        result.append(self._border())


class _Title(_TextSection):
    def __init__(self, grid, caption):
        super(_Title, self).__init__(grid)
        self._caption=caption

    @classmethod
    def _new(cls, size, caption):
        return _Title(_TextGrid(size), caption)

    def _render(self, result):
        result.append(self._caption.center(self._width()))
        result.append(self._border())

    def _width(self):
        return len(self._border())


class _Note(_Title):
    @classmethod
    def _new(cls, size, caption):
        return _Note(_TextGrid(size), caption)

    def _render(self, result):
        result.append(self._caption.ljust(self._width()))

################################################################################

class _XmlReport(_Report):
    def __init__(self):
        super(_XmlReport, self).__init__()
        self.__row=None

    def _empty(self):
        return _Xsd(self)._handle_empty()._render()

    def _render_(self):
        return _Xsd(self)._handle()._render()

    def _xml_(self, nodes):
        result=[node._handle(self) for node in nodes]
        return _XmlNode('xml', [i for i in result if i !=None])

    def _parts_(self, node):
        result=[]
        for (_, line) in self._body():
            self.__row=line
            result.append(node._handle(self))
        return _XmlNode('parts', result)

    def _part_(self):
        return _XmlNode('part', self.__elements())

    def _totals_(self):
        totals=self._totals()
        if len(totals) == 0: return None
        self.__row=totals
        return _XmlNode('totals', self.__elements())

    def __elements(self):
        return [_XmlElement(i.name, j) for (i, j) in self.__row.items()]

################################################################################

class _Xsd:
    def __init__(self, report):
        self.__report=report

    def _handle(self):
        return self.__handle([_XmlParts, _XmlTotals])

    def _handle_empty(self):
        return self.__handle([])

    def __handle(self, nodes):
        return self.__report._xml_(nodes)


class _XmlParts:
    @classmethod
    def _handle(cls, report):
        return report._parts_(_XmlPart)


class _XmlPart:
    @classmethod
    def _handle(cls, report):
        return report._part_()


class _XmlTotals:
    @classmethod
    def _handle(cls, report):
        return report._totals_()

################################################################################

class _Xml(object):
    def __init__(self, tag):
        self.__tag=tag

    def _render(self):
        pass

    def _element(self, value):
        return '<' + self.__tag + '>' + value + '</' + self.__tag + '>'


class _XmlNode(_Xml):
    def __init__(self, tag, children):
        super(_XmlNode, self).__init__(tag)
        self.__children=children

    def _render(self):
        sep='\n' if len(self.__children) > 0 else ''
        value=sep + sep.join([i._render() for i in self.__children]) + sep
        return self._element(value)


class _XmlElement(_Xml):
    def __init__(self, tag, value):
        super(_XmlElement, self).__init__(tag)
        self.__value=value

    def _render(self):
        return self._element(str(self.__value))

################################################################################

