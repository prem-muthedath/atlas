#!/usr/bin/python

class Cost:
	def __init__(self, value=0):
		self.__value=value

	def add(self, cost):
		self.__value+=cost

	def add_to(self, part_schema):
		part_schema.add_cost(self.__class__(self.__value))

	def export(self, exporter):
		return exporter.cost(self.__str__())		

	def __str__(self):
		return str(self.__value)


class UnitCost:
	def __init__(self, value):
		self.__value=value

	def cost(self, quantity):
		return quantity.cost(self.__value)

	def add_to(self, part_schema):
		part_schema.add_unit_cost(self)

	def export(self, exporter):
		return exporter.unit_cost(self.__str__())		

	def __str__(self):
		return str(self.__value)
