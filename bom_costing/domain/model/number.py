#!/usr/bin/python

class Number:
	def __init__(self, number):
		self.__number=number

	def add_to(self, part_schema):
		part_schema.add_number(self)

	def export(self, exporter):
		return exporter.number(self.__number)