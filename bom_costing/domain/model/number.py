#!/usr/bin/python

class Number:
	def __init__(self, number):
		self.__number=number

	def add_to(self, part_schema):
		part_schema.add_number(self)

	def build(self, builder):
		return builder.number(self.__number)