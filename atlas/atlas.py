#!/usr/bin/python

from .database import _AtlasDB
from .configuration import _BomBuilder
from .schema import _Schema
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
        builder=_BomBuilder()
        parts=_AtlasDB()._dump()
        for part in parts:
            builder._add_item(
                    part[_Schema.level],
                    part[_Schema.part_number],
                    part[_Schema.source_code],
                    part[_Schema.unit_cost],
                    part[_Schema.quantity]
                )
        return builder.build()


