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

	def cost(self, cost, quantity):
		quantity.cost(cost, self.__unit_cost)

	def add_to(self, part_builder):
		part_builder.add(self.__dict__.values())
