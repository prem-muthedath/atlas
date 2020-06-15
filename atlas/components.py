#!/usr/bin/python

from collections import OrderedDict

from .schema import _Schema, Costed

################################################################################

class Bom:
    def __init__(self):
        self.__components=[]
        self.__cpos=_BomCostPositions(self)

    def add(self, component):
        if component in self.__components:
            raise RuntimeError("duplicate part")
        self.__components.append(component)
        self.__cpos._new(self.__leaf())

    def __leaf(self):
        return len(self.__components) - 1

    def _new_costed(self):
        return self.__components[-1]._is_costed()

    def _is_costed(self):
        return False

    def cost(self):
        cost=0
        for each in self.__components:
            cost+=each.cost()
        return cost

    def _costable(self, part):
        pos=self.__components.index(part)
        if pos == self.__leaf() or part._costable():
            return self.__cpos._costable(pos)
        return False

    def _positions(self):
        return range(0, self.__leaf() + 1)

    def schema_map(self, level=-1):
        parts=[]
        for each in self.__components:
            part=each.schema_map(level+1)
            if isinstance(part, list):
                parts=parts+part
            else:
                parts.append(part)
        return parts

################################################################################

class _BomCostPositions:
    def __init__(self, bom):
        self.__bom=bom
        self.__pos={'costed' : -1, 'costable' : -1}

    def _new(self, leaf):
        if self.__update_costed():
            self.__pos['costed']=leaf
        if self.__update_costable(leaf-1):
            self.__pos['costable']=-1

    def __update_costed(self):
        return self.__not_costed() and self.__bom._new_costed()

    def __not_costed(self):
        return not self.__has_costed()

    def __has_costed(self):
        return self.__pos['costed'] >= 0

    def __update_costable(self, old_leaf):
        return self.__has_costable() and \
                self.__pos['costable'] == old_leaf

    def __has_costable(self):
        return self.__pos['costable'] >= 0

    def _costable(self, pos):
        if pos in self.__costables():
            self.__pos['costable']=pos
        return self.__pos['costable'] == pos

    def __costables(self):
        if self.__has_costable():
            return [self.__pos['costable']]
        if self.__has_costed():
            return range(0, self.__pos['costed'])
        return self.__bom._positions()

################################################################################

class _Part:
    def __init__(self, bom, number, site, cost, units):
        self.__attr=dict(
                bom=bom,
                number=number,
                site=site,
                cost=cost,
                units=units
            )

    def cost(self):
        if self._is_costed() or self.__attr['bom']._costable(self):
            return self.__cost()
        return 0

    def _is_costed(self):
        return self.__attr['site'] == '12'

    def _costable(self):
        return self.__attr['site'] == '1'

    def __cost(self):
        return self.__attr['units']*self.__attr['cost']

    def schema_map(self, level):
        _cost, _part = self.cost(), OrderedDict()
        for i, item in enumerate(_Schema):
            if item == _Schema.level and item._type == int:
                _part[item]=level
            elif item == _Schema.part_number and item._type == str:
                _part[item]=self.__attr['number']
            elif item == _Schema.source_code and item._type == str:
                _part[item]=self.__attr['site']
            elif item == _Schema.unit_cost and item._type == int:
                _part[item]=self.__attr['cost']
            elif item == _Schema.quantity and item._type == int:
                _part[item]=self.__attr['units']
            elif item == _Schema.costed and item._type == Costed:
                _part[item]=Costed.YES if _cost == self.__cost() else Costed.NO
            elif item == _Schema.cost and item._type == int:
                _part[item]=_cost
            if i == len(_Schema) - 1 and _part.keys() != list(_Schema):
                raise RuntimeError("schema violation in part export")
        return _part

################################################################################


