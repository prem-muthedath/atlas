#!/usr/bin/python

from .schema import _Schema, Costed
from database import _AtlasDB

################################################################################

class _BomCostPositions:
    def __init__(self):
        self.__pos={'costed' : -1, 'costable' : -1}

    def _costed(self, pos):
        if self.__not_costed():
            self.__pos['costed'] = pos

    def __not_costed(self):
        return not self.__has_costed()

    def __has_costed(self):
        return self.__pos['costed'] >= 0

    def _costable(self, pos):
        if self.__has_costable():
            return pos in [self.__pos['costable']]
        if self.__has_costed():
            return pos in range(0, self.__pos['costed'])
        self.__pos['costable']=pos
        return self.__pos['costable'] == pos

    def __has_costable(self):
        return self.__pos['costable'] >= 0

################################################################################

class _Bom:
    def __init__(self, parts):
        self.__components=[]
        for i, val in enumerate(parts):
            if isinstance(val, list):
                self.__components.append(_Bom(val))
            elif i < len(parts) - 1:
                self.__components.append(_Part(self, val))
            else:
                self.__components.append(_LeafPart(self, val))
        self.__cpos=_BomCostPositions()

    def _cost(self):
        cost=0
        for each in self.__components:
            cost+=each._cost()
        return cost

    def _costed(self, part):
        pos=self.__components.index(part)
        self.__cpos._costed(pos)

    def _costable(self, part):
        pos=self.__components.index(part)
        return self.__cpos._costable(pos)

    def _schema_map(self):
        parts=[]
        self._map_(parts)   # collector pattern
        return parts

    def _map_(self, parts):
        for each in self.__components:
            each._map_(parts)

################################################################################

class _Part(object):
    def __init__(self, bom, (number, level, source_code)):
        self.__bom=bom
        self.__number, self.__level, self.__source_code=(number, level, source_code)

    def _cost(self):
        part_map=self.__query()
        return self.__cost_map(part_map)[_Schema.cost]

    def __query(self):
        return _AtlasDB()._part_map(self.__number, self.__level)

    def __cost_map(self, part_map):
        return _CostUnits(
                part_map[_Schema.quantity],
                part_map[_Schema.unit_cost]
            )._cost_map(self)

    def _can_cost(self):
        return self._costed() or self._costable()

    def _costed(self):
        if self.__source_code=='12':
            self.__bom._costed(self)
            return True
        return False

    def _costable(self):
        if self.__source_code=='1':
            return self._bom_costable()
        return False

    def _bom_costable(self):
        return self.__bom._costable(self)

    def _map_(self, parts):
        part_map=self.__query()
        part_map.update(self.__cost_map(part_map))
        parts.append(part_map)

################################################################################

class _LeafPart(_Part):
    def _costable(self):
        return self._bom_costable()

################################################################################

class _CostUnits:
    def __init__(self, units, unit_cost):
        self.__units=units
        self.__unit_cost=unit_cost

    def _cost_map(self, part):
        self.__validate()
        if part._can_cost():
            return {_Schema.costed : Costed.YES, _Schema.cost : self.__cost()}
        return {_Schema.costed : Costed.NO, _Schema.cost : 0}

    def __validate(self):
        if _Schema.costed._type != Costed or int != _Schema.cost._type:
            raise RuntimeError("schema type mismatch in cost")

    def __cost(self):
        return self.__units*self.__unit_cost

################################################################################

