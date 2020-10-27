#!/usr/bin/python

from .configuration import _BomBuilder
from .schema import _Schema
from database import _AtlasDB
from .report import (_TextReport, _XmlReport,)

################################################################################

class Atlas:
    def cost(self):
        return self._bom()._cost()

    def text_report(self, schema=_Schema):
        return _TextReport(schema, self.__contents())._render()

    def xml_report(self, schema=_Schema):
        return _XmlReport(schema, self.__contents())._render()

    def __contents(self):
        contents=[]
        part_maps=_AtlasDB()._part_maps()
        for index, cost_map in enumerate(self._bom()._cost_maps()):
            part_map=part_maps[index]
            part_map.update(cost_map)
            contents.append(part_map)
        return contents

    def _bom(self):
        return _BomBuilder()._build()

################################################################################

