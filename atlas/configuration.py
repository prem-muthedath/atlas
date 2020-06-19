#!/usr/bin/python

from .database import _AtlasDB
from .schema import _Schema
from .components import _Bom

################################################################################

class _BomBuilder():
    def __init__(self):
        self.__parents=[]
        self.__parent_level=0

    def _build(self):
        parts=_AtlasDB()._dump()
        for part in parts:
            self.__add_item(
                    part[_Schema.level],
                    part[_Schema.part_number]
                )
        return _Bom(self.__parents[0])

    def __add_item(self, level, number):
        self.__new_level(level)
        self.__parent().append((level, number))
        self.__new_parents()

    def __new_level(self, level):
        self.__parent_level=level

    def __parent(self):
        if self.__new_bom():
            self.__create()
        return self.__parents[self.__parent_level-1]

    def __new_bom(self):
        return self.__parent_level==self.__previous_parent_level()+1

    def __previous_parent_level(self):
        return len(self.__parents)

    def __create(self):
        self.__parents.append([])
        if len(self.__parents) <= 1: return
        self.__parents[-2].append(self.__parents[-1])

    def __new_parents(self):
        self.__parents=self.__parents[0:self.__parent_level]

################################################################################

