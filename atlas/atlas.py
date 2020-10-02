#!/usr/bin/python

from .configuration import _BomBuilder
from .schema import _Schema
from .report import (_TextReport, _XmlReport,)

################################################################################

class Atlas:
    def cost(self):
        return self._bom()._cost()

    def text_report(self, schema=_Schema):
        return _TextReport()._render(self._bom(), schema)

    def xml_report(self, schema=_Schema):
        return _XmlReport()._render(self._bom(), schema)

    def _bom(self):
        return _BomBuilder()._build()

################################################################################

