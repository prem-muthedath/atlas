#!/usr/bin/python

from .configuration import _BomBuilder
from .report import (_TextReport, _XmlReport,)

################################################################################

class Atlas:
    def cost(self):
        return self.__bom()._cost()

    def text_report(self, schema=None):
        return self.__report(_TextReport(), schema)

    def xml_report(self, schema=None):
        return self.__report(_XmlReport(), schema)

    def __report(self, _type, schema):
        if schema:
            return _type._render(self.__bom(), schema)
        return _type._render(self.__bom())

    def __bom(self):
        return _BomBuilder()._build()

################################################################################

