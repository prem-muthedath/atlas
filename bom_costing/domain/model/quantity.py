#!/usr/bin/python

from costs import AssemblyCost

class Quantity:
	def __init__(self, value):
		self.__value=value

	def cost(self, part_cost):
		assembly_cost=AssemblyCost()
		assembly_cost.add_costs(self.__value*[part_cost])
		return assembly_cost

	def export(self, part_view):
		part_view.add_quantity(self.__value)
		