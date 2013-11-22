#!/usr/bin/python

class Cost:
	def __init__(self, value=0):
		self.__value=value

	def add(self, value):
		self.__value+=value

	def add_to(self, part_builder):
		part_builder.add_cost(self.__str__())

	def __str__(self):
		return str(self.__value)


class UnitCost:
	def __init__(self, value):
		self.__value=value

	def cost(self, cost, units):
		cost.add(units*self.__value)

	def add_to(self, part_builder):
		part_builder.add_unit_cost(self.__data())

	def __data(self):
		return str(self.__value)
