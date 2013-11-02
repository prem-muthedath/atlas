#!/usr/bin/python

class Number:
	def __init__(self, number):
		self.__number=number

	def add_to(self, part_builder):
		part_builder.add_number(self)

	def export(self, name, exporter):
		return exporter.property(name, self.__number)