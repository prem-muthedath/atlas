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
    def __init__(self, bom, (level, number)):
        self.__bom=bom
        self.__level, self.__number=(level, number)

    def _cost(self):
        part=self.__query()
        return self.__cost(part)[_Schema.cost]

    def __query(self):
        return _AtlasDB()._part(self.__number, self.__level)

    def __cost(self, part):
        return _PartCost(
                part[_Schema.source_code],
                _CostUnits(
                    part[_Schema.quantity],
                    part[_Schema.unit_cost]
                )
            )._compute(self)

    def _costed(self):
        self.__bom._costed(self)

    def _costable(self, costable):
        if costable:
            return self._bom_costable()
        return False

    def _bom_costable(self):
        return self.__bom._costable(self)

    def _map_(self, parts):
        part=self.__query()
        part.update(self.__cost(part))
        parts.append(part)

################################################################################

class _LeafPart(_Part):
    def _costable(self, costable):
        return self._bom_costable()

################################################################################

class _PartCost:
    def __init__(self, code, cost_units):
        self.__code=code
        self.__cost_units=cost_units

    def _compute(self, part):
        if self.__costed():
            part._costed()
            return self.__result()
        if part._costable(self.__costable()):
            return self.__result()
        return self.__result(False)

    def __costed(self):
        return self.__code == '12'

    def __result(self, flag=True):
        if _Schema.costed._type != Costed or int != _Schema.cost._type:
            raise RuntimeError("schema type mismatch in cost")
        if flag:
            return {_Schema.costed : Costed.YES, _Schema.cost : self.__cost()}
        return {_Schema.costed : Costed.NO, _Schema.cost : 0}

    def __cost(self):
        return self.__cost_units._cost()

    def __costable(self):
        return self.__code == '1'

################################################################################

class _CostUnits:
    def __init__(self, units, unit_cost):
        self.__units=units
        self.__unit_cost=unit_cost

    def _cost(self):
        return self.__units*self.__unit_cost

################################################################################

