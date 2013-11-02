#!/usr/bin/python

import copy
from ..errors import DuplicateError
from costs import Cost

class Bom:
	def __init__(self):
		self.__components=[]

	def add(self, component):
		if component in self.__components: 
			raise DuplicateError(component)
		self.__components.append(component)

	def cost(self, cost):
		for each in self.__components:
			each.cost(cost)	

	def is_costed(self):
		return 0
	
	def costable(self, bom_part): 
		return self.__first_costable(bom_part) and (self.__is_leaf(bom_part) or bom_part.costable())

	def __first_costable(self, bom_part):
		position=self.__components.index(bom_part)
		return 0==len([each for each in self.__components[:position] if each.is_costed()])

	def __is_leaf(self, bom_part):
		return self.__components[-1]==bom_part

	def export(self, level, exporter):
		data=copy.deepcopy(self.__components)
		level.export_bom(data, exporter)

	def add_to(self, part_builder):
		pass		


class BomPart:
	def __init__(self, part, quantity, bom):
		self.__part=part
		self.__quantity=quantity
		self.__bom=bom

	def cost(self, cost):
		if(self.is_costed()): 
			cost.add(self.__part.cost(self.__quantity))

	def is_costed(self): 
		return self.__part.is_costed()  or self.__bom.costable(self)

	def costable(self):
		return self.__part.costable()

	def export(self, level, exporter):
		level.export_part(self.__data(), exporter)

	def __data(self):
		cost=Cost()
		self.cost(cost)	
		return [cost]+self.__dict__.values()
