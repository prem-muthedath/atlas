#!/usr/bin/python

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
	
	def costable(self, part, source_code): 
		return self.__first_costable(part) and (self.__is_leaf(part) or source_code.costable())

	def __first_costable(self, part):
		position=self.__components.index(part)
		return 0==len([each for each in self.__components[:position] if each.is_costed()])

	def __is_leaf(self, part):
		return self.__components[-1]==part

	def export(self, exporter):
		exporter.export_bom(self)

	def export_children(self, exporter):
		for each in self.__components:
			each.export(exporter)	

	def add_to(self, part_builder):
		pass		


class Part:
	def __init__(self, number, sites, units):
		self.__attributes=dict(__number=number, __sites=sites, __units=units)

	def cost(self, cost):
		if not self.is_costed(): return
		self.__attributes['__units'].cost(cost)

	def is_costed(self): 
		return self.__attributes['__sites'].is_costed(self)

	def export(self, exporter):
		exporter.add_part(self.__data())

	def __data(self):
		cost=Cost()
		self.cost(cost)	
		return [cost]+self.__attributes.values()
