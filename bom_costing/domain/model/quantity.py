#!/usr/bin/python

class Quantity:
	def __init__(self, value):
		self.__value=value

	def cost(self, unit_cost):
		return self.__value*unit_cost

	def add_to(self, part_builder):
		part_builder.add_quantity(self)

	def export(self, name, exporter):
		return exporter.build_field(name, self.__data())

	def __data(self):
		return str(self.__value)
		