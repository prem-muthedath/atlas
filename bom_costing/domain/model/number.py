#!/usr/bin/python

class Number:
	def __init__(self, number):
		self.__number=number

	def add_to(self, part_builder):
		part_builder.add_number(self)

	def render(self, format):
		return format.number(self.__number)