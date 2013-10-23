#!/usr/bin/python

from base import Format

class TextFormat(Format):
	def _level(self, level):
		indent=abs(int(level))*"  "
		return (indent+level).ljust(13)

	def _name(self, name):
		return name.center(65)

	def _code(self, code):
		return code.center(10)

	def _quantity(self, quantity):
		return quantity.center(10)

	def _cost(self, cost):
		return cost.center(10)

	def part_string(self, level, name, code, quantity, cost):	
		return super(type(self), self).part_string(level, name, code, quantity, cost)+'\n'

	def _header(self):
		return 'Level'.center(13)+ \
			self._name('Part')+ \
			self._code('Code')+ \
			self._quantity('Quantity')+ \
			self._cost('Cost')+'\n'
