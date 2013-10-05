#!/usr/bin/python

from costs import AssemblyCost

class Quantity:
	def __init__(self, value):
		self.__value=value

	def cost(self, part_cost):
		assembly_cost=AssemblyCost()
		assembly_cost.add_costs(self.__value*[part_cost])
		return assembly_cost

	def export(self, exporter):
		exporter.add_quantity(self.__data())

	def __data(self):
		return str(self.__value)
		