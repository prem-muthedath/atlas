#!/usr/bin/python

from name import Name

class Part:
	def __init__(self, source_code, part_cost):
		self.__source_code=source_code
		self.__part_cost=part_cost

	def is_costed(self):  
		return self.__source_code.is_costed()

	def costable(self):
		return self.__source_code.costable()

	def cost(self, quantity):
		return quantity.cost(self.__part_cost)

	def export(self, part_exporter):
		part_exporter.export_items(self.__data())

	def __data(self):
		return [Name(str(self)), self.__source_code]		
