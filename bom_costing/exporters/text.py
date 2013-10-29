#!/usr/bin/python

from base import Exporter
from base import PartSchema

class TextExporter(Exporter):
	__FIELD_WIDTH=15

	def level(self, level):
		TAB="  "
		indent=abs(int(level))*TAB
		return (indent+level).ljust(self.__FIELD_WIDTH)

	def number(self, number):
		return self.__centered_field(number)

	def code(self, code):
		return self.__centered_field(code)

	def quantity(self, quantity):
		return self.__centered_field(quantity)

	def unit_cost(self, unit_cost):
		return self.__centered_field(unit_cost)

	def cost(self, cost):
		return self.__centered_field(cost)

	def __centered_field(self, value):
		return value.center(self.__FIELD_WIDTH)

	def part(self, mapped_data):
		part=super(type(self), self).part(mapped_data)
		return self._format('', part, '\n')

	def _build(self):
		header=''.join(self.__centered_field(each) for each in PartSchema().headers())+'\n'
		content=super(type(self), self)._build()
		return self._format(header, content, '')
