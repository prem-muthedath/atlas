#!/usr/bin/python

from .schema import _Schema

################################################################################

class _Report(object):
    def __init__(self):
        self.__body=[]

    def _render(self, bom, schema=_Schema):
        for part in bom._schema_map():
            line=[self._element(i.name, part[i]) for i in schema]
            self.__body.append(self._line(line))
        return self.__render()

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

################################################################################

class _TextReport(_Report):
    def __init__(self):
        super(_TextReport, self).__init__()
        self.__headers=[]

    def _element(self, name, value):
        if name not in self.__headers:
            self.__headers.append(name)
        if name == _Schema.level.name:
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
        for name in self.__headers:
            header=self.__centered(self.__capitalize(name))
            __title.append(header)
        return " ".join(__title)

    def __capitalize(self, header):
        return ' '.join(each[:1].upper()+each[1:].lower() \
                for each in header.split('_'))

################################################################################

class _XmlReport(_Report):
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

