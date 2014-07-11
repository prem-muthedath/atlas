#!/usr/bin/python

class Quantity:
	def __init__(self, value):
		self.__value=value

	def cost(self, unit_cost):
		return unit_cost.cost(self.__value)

	def add_to(self, part_builder):
		part_builder.add_quantity(self.__data())

	def __data(self):
		return str(self.__value)
		