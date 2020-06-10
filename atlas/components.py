#!/usr/bin/python

class Bom:
    def __init__(self):
        self.__components=[]
        self.__cpos=_CostPositions(self)

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

    def cost(self, bom=None):
        cost=0
        for each in self.__components:
            cost+=each.cost(self)
        return cost

    def _costable(self, part):
        pos=self.__components.index(part)
        if pos == self.__leaf() or part._costable():
            return self.__cpos._costable(pos)
        return False

    def _positions(self):
        return range(0, self.__leaf() + 1)

    def __str__(self):
        return "BOM: "


class _CostPositions:
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


class _Part:
    def __init__(self, number, site, cost, units):
        self.__attr=dict(
                number=number,
                site=site,
                cost=cost,
                units=units
            )

    def cost(self, bom):
        if self._is_costed() or bom._costable(self):
            return self.__cost()
        return 0

    def _is_costed(self):
        return self.__attr['site'] == '12'

    def _costable(self):
        return self.__attr['site'] == '1'

    def __cost(self):
        return self.__attr['units']*self.__attr['cost']

    def __str__(self):
        return ", ".join([str((x, y)) for (x, y) in self.__attr.items()])


