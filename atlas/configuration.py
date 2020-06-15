#!/usr/bin/python

from .database import _AtlasDB
from .schema import _Schema
from .components import (Bom, _Part,)

class _BomBuilder():
    def __init__(self):
        self.__parents=[Bom()]
        self.__parent_level=0

    def _build(self):
        parts=_AtlasDB()._dump()
        for part in parts:
            self.__add_item(
                    part[_Schema.level],
                    part[_Schema.part_number],
                    part[_Schema.source_code],
                    part[_Schema.unit_cost],
                    part[_Schema.quantity]
                )
        return self.__parents[0]

    def __add_item(self, level, number, code, cost, quantity):
        self.__new_level(level)
        self.__add(number, code, cost, quantity, self.__parent())
        self.__new_parents()

    def __new_level(self, level):
        self.__parent_level=level

    def __add(self, number, code, cost, quantity, bom):
        part=_Part(bom, number, code, cost, quantity)
        bom.add(part)

    def __parent(self):
        if self.__new_bom():
            self.__create()
        return self.__parents[self.__parent_level]

    def __new_bom(self):
        return self.__parent_level==self.__previous_parent_level()+1

    def __previous_parent_level(self):
        return len(self.__parents)-1

    def __create(self):
        self.__parents.append(Bom())
        self.__parents[self.__parent_level-1].add(self.__parents[self.__parent_level])

    def __new_parents(self):
        self.__parents=self.__parents[0:self.__parent_level+1]



