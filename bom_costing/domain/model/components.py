#!/usr/bin/python

import copy
from ..domain.errors import DuplicateError
from costs import AssemblyCost


class Bom:
	def __init__(self):
		self.__components=[]

	def add(self, component):
		if(component in self.__components): raise DuplicateError(component)
		self.__components.append(component)

	def cost(self, assembly_cost):
		for each in self.__components:
			each.cost(assembly_cost)

	def is_costed(self):
		return 0
	
	def is_costed_part(self, bom_part): 
		return self.__first_costable(bom_part) and (self.__is_leaf(bom_part) or bom_part.costable())

	def __first_costable(self, bom_part):
		for each in self.__components:
			if(each==bom_part): break			
			if(each.is_costed()): return 0
		return 1

	def __is_leaf(self, bom_part):
		return self.__components[len(self.__components)-1]==bom_part

	def export(self, bom_view):
		bom_view.export_bom(self.__data())

	def __data(self):
		return copy.deepcopy(self.__components)


class BomPart():
	def __init__(self, part, quantity, bom):
		self.__part=part
		self.__quantity=quantity
		self.__bom=bom

	def cost(self, assembly_cost):
		return assembly_cost.add_cost(self.__actual_cost())

	def __actual_cost(self):
		if(self.is_costed()): 
			return self.__part.cost(self.__quantity)
		return AssemblyCost()

	def is_costed(self): 
		return self.__part.is_costed()  or self.__bom.is_costed_part(self)

	def costable(self):
		return self.__part.costable()

	def export(self, bom_view):
		bom_view.export_part(self.__data())

	def __data(self):
		return [self.__quantity, self.__actual_cost(), self.__part]

