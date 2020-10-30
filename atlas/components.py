#!/usr/bin/python

from .schema import _Schema, Costed
from .database import _AtlasDB

################################################################################

class _BomState:
    def __init__(self):
        self.__pos=-1

    def _costed(self, pos):
        if self.__not_costed():
            self.__pos=pos

    def __not_costed(self):
        return self.__pos < 0

    def _costable(self, pos):
        self._costed(pos)
        return pos == self.__pos

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
        self.__state=_BomState()

    def _cost(self):
        cost=0
        for each in self.__components:
            cost+=each._cost()
        return cost

    def _costed(self, part):
        pos=self.__components.index(part)
        self.__state._costed(pos)

    def _costable(self, part):
        pos=self.__components.index(part)
        return self.__state._costable(pos)

    def _cost_maps(self):
        cost_maps=[]
        self._add_to(cost_maps)   # `collecting parameter` pattern
        return cost_maps

    def _add_to(self, cost_maps):
        for each in self.__components:
            each._add_to(cost_maps)

################################################################################

class _Part:
    def __init__(self, bom, vals):
        self.__bom=bom
        self.__source_code, self.__cost_units=vals

    def _cost(self):
        return self.__cost_map()[_Schema.cost]

    def __cost_map(self):
        return self.__cost_units._cost_map(self)

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

    def _add_to(self, cost_maps):
        cost_maps.append(self.__cost_map())

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
        assert _Schema.costed._type == Costed, 'bad costed type.'
        assert int == _Schema.cost._type, 'cost type not int.'

    def __cost(self):
        return self.__units*self.__unit_cost

################################################################################

