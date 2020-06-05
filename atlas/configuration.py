#!/usr/bin/python

from .components import (Bom, Part,)

class BomBuilder():
    def __init__(self):
        self.__parents=[Bom()]
        self.__parent_level=0

    def add_item(self, level, number, code, cost, quantity):
        self.__new_level(level)
        self.__add(number, code, cost, quantity, self.__parent())
        self.__new_parents()

    def __new_level(self, level):
        self.__parent_level=level

    def __add(self, number, code, cost, quantity, bom):
        part=Part(number, code, cost, quantity)
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

    def build(self):
        return self.__parents[0]


# costable:  P-0007
# costed:  P-0009
# costable:  P-0022
# costable:  P-0023
# costed:  P-0024
# costed:  P-0025

# class Bom:
#     def __init__(self):
#         self.__components=[]
#         self.__costed=False
# 
#     def add(self, component):
#         if component in self.__components: 
#             raise RuntimeError("duplicate part")
#         if component.is_costed():
#             self.__costed=True
#         self.__components.append(component)
# 
#     def is_costed(self):
#         return False
# 
#     def cost(self, bom=None):
#         cost=0
#         for each in self.__components:
#             cost=cost+each.cost(self)
#         return cost
# 
#     def costed(self):
#         self.__costed=True
# 
#     def costable(self, part): 
#         if self.__costed:
#             return False
#         if part == self.__components[-1] or part.costable():
#             self.costed()
#         return self.__costed
# 
# class Part:
#     def __init__(self, number, site, cost, units):
#         self.__attr=dict(
#                 number=number,
#                 site=site,
#                 cost=cost,
#                 units=units
#             )
#         
#     def cost(self, bom):
#         print "part: ", self.__attr.items()
#         if self.is_costed():
#             print "costed: ", self.__attr['number']
#             return self.__cost()
#         if bom.costable(self):
#             print "costable: ", self.__attr['number']
#             return self.__cost()
#         return 0
#         # if self.__attr['site'] == '12':
#         #     bom.costed()
#         #     return self.__attr['units']*self.__attr['cost']
#         # if bom.costable(self):
#         #     return self.__attr['units']*self.__attr['cost']
#         # return 0
# 
#     def __cost(self):
#         return self.__attr['units']*self.__attr['cost']
# 
#     def is_costed(self):
#         return self.__attr['site'] == '12'
# 
#     def costable(self):
#         return self.__attr['site'] == '1'
