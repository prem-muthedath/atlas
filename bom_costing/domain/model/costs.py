#!/usr/bin/python

class Cost:
	def __init__(self, amount=0):
		self.__amount=amount

	def cost(self, part):
		self.__add(part.assembly_cost())

	def __add(self, cost):
		self.__amount+=cost.__amount

	def add_to(self, part_builder):
		part_builder.add_cost(self.__str__())

	def __str__(self):
		return str(self.__amount)


class UnitCost:
	def __init__(self, amount):
		self.__amount=amount

	def cost(self, units):
		return Cost(units*self.__amount)

	def add_to(self, part_builder):
		part_builder.add_unit_cost(self.__data())

	def __data(self):
		return str(self.__amount)
