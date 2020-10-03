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
        return ""

    def _render_(self):
        pass

    def _body(self):
        return [self._line(i+1, line) for i, line in enumerate(self.__contents)]

    def _line(self):
        pass

    def _names(self):
        return self.__contents[0].keys() if len(self.__contents) > 0 else []

    def _totals(self):
        totals=OrderedDict()
        columns=[i for i in _Schema._totals_schema() if i in self._names()]
        for col in columns:
            totals[col]=col._total([line[col] for line in self.__contents])
        return totals

################################################################################

class _TextRow(object):
    def __init__(self, cells):
        self.__cells=cells
        self._field_width=15

    def _render(self):
        return " ".join([self.__centered(i) for i in self.__cells])

    def __centered(self, value):
        return value.center(self._field_width)

    def _size(self):
        return len(self.__cells)

class _Border(_TextRow):
    def __init__(self, cols):
        super(_Border, self).__init__([])
        self.__cols=cols
        self.__symbol='-'

    def _render(self):
        width=self.__cols*self._field_width + 5
        return self.__symbol * width

################################################################################

class _TextReport(_Report):
    def __init__(self):
        super(_TextReport, self).__init__()
        self.__captions={'ITEM' : "item", 'TOTALS' : "totals"}

    def _render_(self):
        contents=self.__bordered(self.__title())
        contents.extend(self.__body())
        contents.extend(self.__bordered(self.__footer()))
        return "\n".join(contents)

    def __title(self):
        headers=[self.__capitalize(i.name) for i in self._names()]
        headers=[self.__capitalize(self.__captions['ITEM'])] + headers
        return _TextRow(headers)._render()

    def __capitalize(self, header):
        return ' '.join(each[:1].upper()+each[1:].lower() \
                for each in header.split('_'))

    def __body(self):
        return [_TextRow(i)._render() for i in self._body()]

    def _line(self, index, line):
        results=[str(index)]
        for (name, value) in line.items():
            if name == _Schema.level:
                indent=(value-1)*"  "
                result=indent+str(value)
            else:
                result=str(value)
            results.append(result)
        return results

    def __footer(self):
        return _TextRow(self._footer())._render()

    def _footer(self):
        totals=self._totals()
        if len(totals) == 0: return []
        __totals=[str(totals[name]) if totals.has_key(name) else " " for name in self._names()]
        return [self.__capitalize(self.__captions['TOTALS'])] + __totals

    def __bordered(self, data):
        border=self.__border()._render()
        if len(data) > 0:
            return [border, data, border]
        return [border]

    def __border(self):
        cols=len(self._names()) + 1
        return _Border(cols)

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
        return self.__element(self.__tags["XML"], "", "")

    def __element(self, name, val, sep=""):
        return '<' + name + '>' +  sep + str(val) + sep + '</' + name + '>'

    def _render_(self):
        xml="\n".join([i for i in [self.__body(), self._footer()] if len(i) > 0])
        return self.__element(self.__tags["XML"], xml, "\n")

    def __body(self):
        body="\n".join([i for i in self._body()])
        return self.__element(self.__tags["PARTS"], body, "\n")

    def _line(self, index, line):
        fline="".join([self.__element(i.name, j) for (i, j) in line.items()])
        return self.__element(self.__tags["PART"], fline)

    def _footer(self):
        totals=self._totals()
        if len(totals) == 0: return ""
        val="".join([self.__element(key.name, totals[key]) for key in totals])
        return self.__element(self.__tags["TOTALS"], val)

################################################################################

