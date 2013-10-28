#!/usr/bin/python

class Part:
	def __init__(self, number, source_code, unit_cost):
		self.__number=number
		self.__source_code=source_code
		self.__unit_cost=unit_cost

	def is_costed(self):  
		return self.__source_code.is_costed()

	def costable(self):
		return self.__source_code.costable()

	def cost(self, quantity):
		return self.__unit_cost.cost(quantity)

	def add_to(self, part_schema):
		part_schema.add(self.__data())

	def __data(self):
		return [self.__number, self.__source_code, self.__unit_cost]		
