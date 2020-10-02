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
            line=[("item", index+1)] + [(i.name, part_map[i]) for i in schema]
            self.__contents.append(line)
        return self.__render()

    def __render(self):
        if self.__contents==[] or len(self.__contents[0]) <= 1:
            return self._empty()
        result = [self._title(), self._body(), self._footer()]
        return "\n".join([i for i in result if len(i) > 0])

    def _empty(self):
        return ""

    def _body(self):
        body=[]
        for line in self.__contents:
            body.append(self._format(line))
        return "\n".join(body)

    def _title(self):
        pass

    def _footer(self):
        pass

    def _names(self):
        if len(self.__contents) > 0:
            return [name for (name, _) in self.__contents[0]]
        return []

    def _totals(self):
        fields=[i.name for i in _Schema._totals_schema() if i.name in self._names()]
        totals=OrderedDict()
        lines=[dict(line) for line in self.__contents]
        for i in fields:
            vals=[line[i] for line in lines if line.has_key(i)]
            if i == _Schema.costed.name:
                totals[i]=sum([1 if str(val) == 'Y' else 0 for val in vals])
            else:
                totals[i]=sum(vals)
        return totals

################################################################################

class _TextReport(_Report):
    def __init__(self):
        super(_TextReport, self).__init__()
        self.__field_width=15

    def _format(self, line):
        results=[]
        for (name, value) in line:
            if name == _Schema.level.name:
                indent=(value-1)*"  "
                result=indent+str(value)
            else:
                result=str(value)
            results.append(self.__centered(result))
        return " ".join(results)

    def __centered(self, value):
        return value.center(self.__field_width)

    def _title(self):
        headers=[]
        for name in self._names():
            header=self.__centered(self.__capitalize(name))
            headers.append(header)
        return self.__result(headers)

    def __capitalize(self, header):
        return ' '.join(each[:1].upper()+each[1:].lower() \
                for each in header.split('_'))

    def __result(self, vals):
        if len(vals) > 0:
            return "\n".join([self.__border(), " ".join(vals), self.__border()])
        return self.__border()

    def __border(self):
        width=len(self._names())*self.__field_width + 5
        return "-" * width

    def _footer(self):
        __totals=[]
        totals=self._totals()
        if len(totals)==0: return self.__result([])
        for name in self._names():
            if name == "item":
                total="Totals"
            elif totals.has_key(name):
                total=str(totals[name])
            else:
                total=" "
            __totals.append(self.__centered(total))
        return self.__result(__totals)

################################################################################

class _XmlReport(_Report):
    def _empty(self):
        return self.__element("xml", "")

    def _body(self):
        body=super(_XmlReport, self)._body()
        if len(body) > 0:
            return '\n'.join(['<parts>', body, '</parts>'])
        return body

    def _format(self, line):
        fline=[]
        for (name, value) in line:
            if name=="item": continue
            fline.append(self.__element(name, value))
        return self.__element("part", "".join(fline))

    def __element(self, name, val):
        return '<' + name + '>' + str(val) + '</' + name + '>'

    def _title(self):
        return '<xml>'

    def _footer(self):
        totals=self._totals()
        val=[]
        for name in self._names():
            if totals.has_key(name):
                val.append(self.__element(name, totals[name]))
        data=self.__element("totals", "".join(val))
        return "\n".join([data, "</xml>"]) if len (val) > 0 else "</xml>"

################################################################################
