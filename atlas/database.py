#!/usr/bin/python

from .schema import _Schema

class _AtlasDB:
    __parts = [ # represents the database
        [("name", "P-0001"), ("level", 1), ("site", '1'), ("cost", 1000), ("units", 2)],    # 1000*2
        [("name", "P-0002"), ("level", 1), ("site", '1'), ("cost", 1000), ("units", 2)],    # dup: uncosted
        [("name", "P-0003"), ("level", 2), ("site", '120'), ("cost", 2000), ("units", 2)],
        [("name", "P-0004"), ("level", 2), ("site", '11'), ("cost", 1500), ("units", 1)],
        [("name", "P-0005"), ("level", 2), ("site", '78'), ("cost", 100), ("units", 1)],
        [("name", "P-0006"), ("level", 2), ("site", '007'), ("cost", 700), ("units", 2)],   # dup to leaf below
        [("name", "P-0007"), ("level", 2), ("site", '007'), ("cost", 700), ("units", 2)],   # 700*2; leaf @ lvl 2
        [("name", "P-0008"), ("level", 1), ("site", '13'), ("cost", 1000), ("units", 1)],
        [("name", "P-0009"), ("level", 2), ("site", '12'), ("cost", 2000), ("units", 1)],   # 2000*1
        [("name", "P-0010"), ("level", 2), ("site", '15'), ("cost", 1500), ("units", 3)],
        [("name", "P-0011"), ("level", 2), ("site", '48'), ("cost", 1000), ("units", 1)],
        [("name", "P-0012"), ("level", 2), ("site", '8'), ("cost", 1), ("units", 1)],
        [("name", "P-0013"), ("level", 2), ("site", '007'), ("cost", 700), ("units", 1)],
        [("name", "P-0014"), ("level", 1), ("site", '13'), ("cost", 1000), ("units", 2)],
        [("name", "P-0015"), ("level", 2), ("site", '144'), ("cost", 2000), ("units", 1)],
        [("name", "P-0016"), ("level", 2), ("site", '15'), ("cost", 1500), ("units", 1)],
        [("name", "P-0017"), ("level", 2), ("site", '48'), ("cost", 1000), ("units", 1)],
        [("name", "P-0018"), ("level", 2), ("site", '8'), ("cost", 1), ("units", 1)],
        [("name", "P-0019"), ("level", 2), ("site", '007'), ("cost", 700), ("units", 1)],   # not leaf @ lvl 2
        [("name", "P-0020"), ("level", 3), ("site", '135'), ("cost", 1000), ("units", 1)],
        [("name", "P-0021"), ("level", 3), ("site", '400'), ("cost", 10), ("units", 1)],
        [("name", "P-0022"), ("level", 3), ("site", '600'), ("cost", 2000), ("units", 1)],  # 2000*1; leaf @ lvl 3
        [("name", "P-0023"), ("level", 2), ("site", '007'), ("cost", 800), ("units", 1)],   # 800*1; leaf @ lvl 2
        [("name", "P-0024"), ("level", 1), ("site", '12'), ("cost", 1), ("units", 5)],      # 1*5
        [("name", "P-0025"), ("level", 1), ("site", '12'), ("cost", 1), ("units", 5)],      # 1*5
        [("name", "P-0026"), ("level", 1), ("site", '145'), ("cost", 90), ("units", 1)],    # not costed
        [("name", "P-0027"), ("level", 1), ("site", '165'), ("cost", 900), ("units", 1)]
    ]

    @classmethod
    def _dump(cls):
        parts=[]
        for part in cls.__parts:
            parts.append(cls.__map(part[:]))
        return parts

    @classmethod
    def __map(cls, _part):
        part={}
        for i, (name, val) in enumerate(_part):
            if name == 'name' and type(val) == _Schema.part_number._type:
                part[_Schema.part_number]=val
            elif name == 'level' and type(val) == _Schema.level._type:
                part[_Schema.level]=val
            elif name == 'site' and type(val) == _Schema.source_code._type:
                part[_Schema.source_code]=val
            elif name == 'cost' and type(val) == _Schema.unit_cost._type:
                part[_Schema.unit_cost]=val
            elif name == 'units' and type(val) == _Schema.quantity._type:
                part[_Schema.quantity]=val
            if i == len(_part) - 1 and len(part) != len(_part):
                raise RuntimeError("DB schema map error")
        return part

