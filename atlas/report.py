#!/usr/bin/python

from .schema import _Schema

class TextReport:
    def __init__(self, headers=list(_Schema)):
        self.__headers=headers
        self.__body=[]

    def render(self, bom):
        for part in bom.export():
            self.__add(part)
        return self.__print()

    def __add(self, part):
        line=[]
        for item in self.__headers:
            val = part[item]
            line.append(self.__position(item, val))
        self.__body.append(" ".join(line))

    def __position(self, item, value):
        if item.name == 'level':
            indent=(value-1)*"  "
            return (indent+str(value)).center(self.__fwidth())
        return self.__centered(str(value))

    def __fwidth(self):
        return 15

    def __centered(self, value):
        return value.center(self.__fwidth())

    def __print(self):
        return self.__title() + "\n" + "\n".join(self.__body)

    def __title(self):
        _title=[]
        for item in self.__headers:
            header=self.__centered(self.__capitalize(item.name))
            _title.append(header)
        return " ".join(_title)

    def __capitalize(self, header):
        return ' '.join(each[:1].upper()+each[1:].lower() for each in header.split('_'))


class XmlReport:
    def __init__(self, headers=list(_Schema)):
        self.__headers=headers
        self.__body=[]

    def render(self, bom):
        for part in bom.export():
            self.__add(part)
        return self.__print()

    def __add(self, part):
        line=[]
        for item in self.__headers:
            val = part[item]
            line.append(self.__element(item.name, val))
        self.__add_line(line)

    def __element(self, name, val):
        return '<' + name + '>' + str(val) + '</' + name + '>'

    def __add_line(self, line):
        _line="".join(line)
        return self.__body.append(self.__element("part", _line))

    def __print(self):
        return '<xml>' + "\n" + \
                "\n".join(self.__body) + "\n" + \
                "</xml>"

