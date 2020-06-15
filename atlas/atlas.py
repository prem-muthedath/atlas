#!/usr/bin/python

from .configuration import _BomBuilder
from .report import (TextReport, XmlReport,)

class Atlas:
    def cost(self):
        return self.__bom().cost()

    def text_report(self, schema=None):
        report=TextReport()
        if schema:
            return report.render(self.__bom(), schema)
        return report.render(self.__bom())

    def xml_report(self, schema=None):
        report=XmlReport()
        if schema:
            return report.render(self.__bom(), schema)
        return report.render(self.__bom())

    def __bom(self):
        return _BomBuilder()._build()


