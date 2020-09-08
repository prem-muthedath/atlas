#!/usr/bin/python

from .configuration import _BomBuilder
from .report import (_TextReport, _XmlReport,)

################################################################################

class Atlas:
    def cost(self):
        return self._bom()._cost()

    def text_report(self, schema=None):
        return self.__report(_TextReport(), schema)

    def xml_report(self, schema=None):
        return self.__report(_XmlReport(), schema)

    def __report(self, _type, schema):
        if schema:
            return _type._render(self._bom(), schema)
        return _type._render(self._bom())

    def _bom(self):
        return _BomBuilder()._build()

################################################################################

