#!/usr/bin/python

class Quantity:
	def __init__(self, value):
		self.__value=value

	def cost(self, unit_cost):
		return self.__value*unit_cost

	def add_to(self, part_schema):
		part_schema.add_quantity(self)

	def export(self, exporter):
		return exporter.quantity(self.__data())

	def __data(self):
		return str(self.__value)
		