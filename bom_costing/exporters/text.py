#!/usr/bin/python

from base import Exporter
from base import PartSchema
import string

class TextExporter(Exporter):
	__FIELD_WIDTH=15

	def level(self, level):
		indent=abs(int(level))*"  "
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
		header=''.join(self.__field_header(each) for each in PartSchema.fields())+'\n'
		content=super(type(self), self)._build()
		return self._format(header, content, '')

	def __field_header(self, field):
		punc=string.punctuation
		cleaned_field=''.join(each if each not in punc else ' ' for each in list(field))
		capitilized_header=' '.join(each[:1].upper()+each[1:] for each in cleaned_field.split())
		return self.__centered_field(capitilized_header)
