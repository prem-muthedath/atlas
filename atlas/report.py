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
        return [(i+1, line) for i, line in enumerate(self.__contents)]

    def _names(self):
        return self.__contents[0].keys() if len(self.__contents) > 0 else []

    def _totals(self):
        totals=OrderedDict()
        columns=[i for i in _Schema._totals_schema() if i in self._names()]
        for col in columns:
            totals[col]=col._total([line[col] for line in self.__contents])
        return totals

################################################################################

class _TextReport(_Report):
    def _empty(self):
        return ""

    def _render_(self):
        captions={'ITEM' : "item", 'TOTALS' : "totals"}
        return _TextView(
            _Header(captions['ITEM'], self._names()),
            self.__body(),
            _Footer(captions['TOTALS'], self._names(), self._totals())
        )._render()

    def __body(self):
        results=[self.__line(i, line) for (i, line) in self._body()]
        return [_TextRow(i) for i in results]

    def __line(self, index, line):
        results=[str(index)]
        for (name, value) in line.items():
            if name == _Schema.level:
                indent=(value-1)*"  "
                result=indent+str(value)
            else:
                result=str(value)
            results.append(result)
        return results

################################################################################

class _TextView:
    def __init__(self, header, body, footer):
        self.__header=header
        self.__body=body
        self.__footer=footer

    def _render(self):
        data=self.__header._render()
        data.extend([i._render() for i in self.__body])
        data.extend(self.__footer._render())
        return "\n".join(data)

################################################################################

class _Header(object):
    def __init__(self, tag, cols):
        self.__tag=tag
        self.__cols=cols

    def _render(self):
        return self._render_(self.__headers())

    def _render_(self, items):
        data=[self._capitalize()] + items
        return self._bordered(_TextRow(data))._render()

    def __headers(self):
        return [self._capitalize(i.name) for i in self.__cols]

    def _capitalize(self, word=None):
        word=self.__tag if word==None else word
        return ' '.join(each[:1].upper()+each[1:].lower() \
                for each in word.split('_'))

    def _bordered(self, row):
        tag_col= 1 if self.__tag != None else 0
        cells=[""]*(len(self.__cols) + tag_col)
        return _BorderedRow(cells, row)

    def _matches(self, cols):
        return [col if col in cols else None for col in self.__cols]


class _Footer(_Header):
    def __init__(self, tag, cols, totals):
        super(_Footer, self).__init__(tag, cols)
        self.__totals=totals

    def _render(self):
        if len(self.__totals) == 0:
            return self._bordered(_TextRow([]))._render()
        return self._render_(self.__footers())

    def __footers(self):
        matches=self._matches(self.__totals.keys())
        return [" " if i==None else str(self.__totals[i]) for i in matches]

################################################################################

class _TextRow(object):
    def __init__(self, cells):
        self.__cells=cells
        self.__field_width=15

    def _render(self):
        return " ".join([self.__centered(i) for i in self.__cells])

    def __centered(self, value):
        return value.center(self.__field_width)

    def _width(self):
        return len(self.__cells)*self.__field_width


class _BorderedRow(_TextRow):
    def __init__(self, cells, row):
        super(_BorderedRow, self).__init__(cells)
        self.__row=row
        self.__symbol='-'

    def _render(self):
        data=self.__row._render()
        if len(data) > 0:
            return [self.__border(), data, self.__border()]
        return [self.__border()]

    def __border(self):
        width=self._width() + 5
        return self.__symbol * width

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

