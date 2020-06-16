#!/usr/bin/python

from .schema import _Schema, Costed

################################################################################

class _Bom:
    def __init__(self):
        self.__components=[]
        self.__cpos=_BomCostPositions(self)

    def _add(self, component):
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

    def _cost(self):
        cost=0
        for each in self.__components:
            cost+=each._cost()
        return cost

    def _costable(self, part):
        pos=self.__components.index(part)
        if pos == self.__leaf() or part._costable():
            return self.__cpos._costable(pos)
        return False

    def _positions(self):
        return range(0, self.__leaf() + 1)

    def _schema_map(self):
        parts=[]
        self._map_(-1, parts)   # collector pattern
        return parts

    def _map_(self, level, parts):
        for each in self.__components:
            each._map_(level+1, parts)

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
    def __init__(self, bom, number, site, cost_units):
        self.__bom=bom
        self.__attr={'number' : number, 'site' : site, 'costunits' : cost_units}

    def _cost(self):
        if self._is_costed() or self.__bom._costable(self):
            return self.__attr['costunits']._cost()
        return 0

    def _is_costed(self):
        return self.__attr['site'] == '12'

    def _costable(self):
        return self.__attr['site'] == '1'

    def _map_(self, level, parts):
        _map={_Schema.level : level} if type(level)==_Schema.level._type else {}
        for i, (name, val) in enumerate(self.__attr.items()):
            if name == 'number' and type(val) == _Schema.part_number._type:
                _map[_Schema.part_number]=val
            elif name == 'site' and type(val) == _Schema.source_code._type:
                _map[_Schema.source_code]=val
            elif name == 'costunits':
                _map.update(val._map_(self))
            if i == len(self.__attr) - 1 and len(_map) != len(_Schema):
                raise RuntimeError("part schema map error")
        parts.append(_map)

    def __eq__(self, other):
        if not isinstance(other, _Part):
            return False
        return self.__attr['number'] == other.__attr['number']

    def __ne__(self, other):
        return not self == other

################################################################################

class _CostUnits:
    def __init__(self, unit_cost, units):
        self.__unit_cost=unit_cost
        self.__units=units

    def _cost(self):
        return self.__units*self.__unit_cost

    def _map_(self, part):
        return self.__map(part._cost(), {})

    def __map(self, cst, _map):
        if type(cst) == _Schema.cost._type:
            _map[_Schema.cost]=cst
        if _Schema.costed._type == Costed:
            _map[_Schema.costed]=Costed.YES if cst==self._cost() else Costed.NO
        if type(self.__unit_cost) == _Schema.unit_cost._type:
            _map[_Schema.unit_cost]=self.__unit_cost
        if type(self.__units) == _Schema.quantity._type:
            _map[_Schema.quantity]=self.__units
        return _map

################################################################################


