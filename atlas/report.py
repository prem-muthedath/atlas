#!/usr/bin/python

from .schema import _Schema
from database import _AtlasDB

from collections import OrderedDict

################################################################################

class _Report(object):
    def __init__(self):
        self.__contents=[]

    def _render(self, bom, schema=_Schema):
        part_maps=_AtlasDB()._part_maps()
        for index, cost_map in enumerate(bom._cost_maps()):
            part_map=part_maps[index]
            part_map.update(cost_map)
            line=OrderedDict([(i, part_map[i]) for i in schema])
            self.__contents.append(line)
        return self.__render()

    def __render(self):
        if len(self.__contents) == 0 or len(self._names()) == 0:
            return self._empty()
        return self._render_()

    def _empty(self):
        return ""

    def _render_(self):
        pass

    def _body(self):
        body=[]
        for i, line in enumerate(self.__contents):
            body.append(self._format(i+1, line))
        return body

    def _names(self):
        return self.__contents[0].keys() if len(self.__contents) > 0 else []

    def _totals(self):
        fields=[i for i in self._names() if i in _Schema._totals_schema()]
        totals=OrderedDict()
        for i in fields:
            vals=[line[i] for line in self.__contents]
            if i == _Schema.costed:
                totals[i]=sum([1 if str(val) == 'Y' else 0 for val in vals])
            else:
                totals[i]=sum(vals)
        return totals

################################################################################

class _TextView():
    def __init__(self):
        self.__field_width=15

    def _render(self, title, body, footer):
        cols=len(title)
        tv=self.__format(title, cols)
        bv="\n".join([" ".join([self.__centered(j) for j in i]) for i in body])
        fv=self.__format(footer, cols)
        return "\n".join([i for i in [tv, bv, fv] if len(i) > 0])

    def __centered(self, value):
        return value.center(self.__field_width)

    def __format(self, vals, cols):
        width=cols*self.__field_width + 5
        border="-" * width
        if len(vals) > 0:
            data=" ".join([self.__centered(i) for i in vals])
            return "\n".join([border, data, border])
        return border

################################################################################

class _TextReport(_Report):
    def _render_(self):
        title=self._title()
        body=self._body()
        footer=self._footer()
        return _TextView()._render(title, body, footer)

    def _format(self, index, line):
        results=[str(index)]
        for (name, value) in line.items():
            if name == _Schema.level:
                indent=(value-1)*"  "
                result=indent+str(value)
            else:
                result=str(value)
            results.append(result)
        return results

    def _title(self):
        headers=[self.__capitalize(i.name) for i in self._names()]
        headers=[self.__capitalize("item")] + headers
        return headers

    def __capitalize(self, header):
        return ' '.join(each[:1].upper()+each[1:].lower() \
                for each in header.split('_'))

    def _footer(self):
        totals=self._totals()
        if len(totals) == 0: return []
        __totals=[str(totals[name]) if totals.has_key(name) else " " for name in self._names()]
        __totals=["Totals"] + __totals
        return __totals

################################################################################

class _XmlReport(_Report):
    def _empty(self):
        return self.__element("xml", "", "")

    def _render_(self):
        body="\n".join([i for i in self._body()])
        bv=self.__element("parts", body, "\n")
        fv=self._footer()
        cont="\n".join([i for i in [bv, fv] if len(i) > 0])
        return self.__element("xml", cont, "\n")

    def _format(self, index, line):
        fline=[]
        for (name, value) in line.items():
            fline.append(self.__element(name.name, value))
        return self.__element("part", "".join(fline))

    def __element(self, name, val, sep=""):
        return '<' + name + '>' +  sep + str(val) + sep + '</' + name + '>'

    def _footer(self):
        totals=self._totals()
        if len(totals) == 0: return ""
        val=[self.__element(key.name, totals[key]) for key in totals]
        return self.__element("totals", "".join(val))

################################################################################
