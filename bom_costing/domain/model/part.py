#!/usr/bin/python

class Part:
	def __init__(self, number, source_code, cost):
		self.__number=number
		self.__source_code=source_code
		self.__cost=cost

	def is_costed(self):  
		return self.__source_code.is_costed()

	def costable(self):
		return self.__source_code.costable()

	def cost(self, quantity):
		return quantity.cost(self.__cost)

	def add_to(self, part_builder):
		part_builder.add(self.__data())

	def __data(self):
		return [self.__number, self.__source_code]		
