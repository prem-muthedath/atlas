#!/usr/bin/python

from .schema import _Schema

################################################################################

class Report:
    def __init__(self, headers=list(_Schema)):
        self.__headers=headers
        self.__body=[]

    def render(self, bom):
        for part in bom.schema_map():
            self.__add(part)
        return self.__render()

    def __add(self, part):
        line=[]
        for item in self.__headers:
            val = part[item]
            line.append(self._element(item.name, val))
        self.__body.append(self._line(line))

    def _element(self, name, val):
        pass

    def _line(self, line):
        pass

    def __render(self):
        return self._title() + "\n" + "\n".join(self.__body) + self._footer()

    def _title(self):
        pass

    def _footer(self):
        return ""

    def _headers(self):
        return [header.name for header in self.__headers]

################################################################################

class TextReport(Report):
    def _element(self, name, value):
        if name == 'level':
            indent=(value-1)*"  "
            return self.__centered(indent+str(value))
        return self.__centered(str(value))

    def __centered(self, value):
        return value.center(self.__field_width())

    def __field_width(self):
        return 15

    def _line(self, line):
        return " ".join(line)

    def _title(self):
        __title=[]
        for name in self._headers():
            header=self.__centered(self.__capitalize(name))
            __title.append(header)
        return " ".join(__title)

    def __capitalize(self, header):
        return ' '.join(each[:1].upper()+each[1:].lower() \
                for each in header.split('_'))

################################################################################

class XmlReport(Report):
    def _element(self, name, val):
        return '<' + name + '>' + str(val) + '</' + name + '>'

    def _line(self, line):
        __line="".join(line)
        return self._element("part", __line)

    def _title(self):
        return '<xml>'

    def _footer(self):
        return "\n" + "</xml>"

################################################################################

