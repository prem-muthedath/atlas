#!/usr/bin/python

class Bom:
    def __init__(self):
        self.__components=[]
        self.__costed_pos=-1
        self.__costable_pos=-1

    def add(self, component):
        if component in self.__components: 
            raise RuntimeError("duplicate part")
        if self.__costed_pos < 0 and component.is_costed():
            self.__costed_pos=len(self.__components)
        self.__components.append(component)

    def is_costed(self):
        return False

    def cost(self, bom=None):
        cost=0
        for each in self.__components:
            cost=cost+each.cost(self)
        self.reset()
        return cost

    def reset(self):
        self.__costable_pos=-1

    def costable(self, part): 
        pos=self.__components.index(part)
        if self.__costed_pos >= 0 and pos > self.__costed_pos:
            return False
        if self.__costable_pos >= 0:
            return False
        if pos == len(self.__components)-1 or part.costable():
            self.__costable_pos=pos
        return self.__costable_pos==pos
    
    def __str__(self):
        return "BOM: "


class Part:
    def __init__(self, number, site, cost, units):
        self.__attr=dict(
                number=number,
                site=site,
                cost=cost,
                units=units
            )
        
    def cost(self, bom):
        if self.is_costed() or bom.costable(self):
            return self.__cost()
        return 0

    def __cost(self):
        return self.__attr['units']*self.__attr['cost']

    def is_costed(self):
        return self.__attr['site'] == '12'

    def costable(self):
        return self.__attr['site'] == '1'
    
    def __str__(self):
        return ", ".join([str((x, y)) for (x, y) in self.__attr.items()])

# class Bom:
#     def __init__(self):
#         self.__components=[]
#         self.__costed=False
# 
#     def add(self, component):
#         if component in self.__components: 
#             raise RuntimeError("duplicate part")
#         self.__components.append(component)
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
#         leaf = part == self.__components[-1]
#         if leaf or part.costable():
#             self.costed()
#             return True
#         return False
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
#         if self.__attr['site'] == '12':
#             bom.costed()
#             return self.__attr['units']*self.__attr['cost']
#         if bom.costable(self):
#             return self.__attr['units']*self.__attr['cost']
#         return 0
# 
#     def costable(self):
#         return self.__attr['site'] == '1'



