#!/usr/bin/python

from base import Builder

class TextBuilder(Builder):
	def level(self, level):
		indent=abs(int(level))*"  "
		return (indent+level).ljust(13)

	def number(self, number):
		return number.center(10)

	def code(self, code):
		return code.center(10)

	def quantity(self, quantity):
		return quantity.center(10)

	def unit_cost(self, unit_cost):
		return unit_cost.center(10)

	def cost(self, cost):
		return cost.center(10)

	def part(self, mapped_data):
		return self._part('', mapped_data, '\n')

	def build(self):
		header='Level'.center(13)+ \
			self.number('Part')+ \
			self.code('Code')+ \
			self.unit_cost('Unit Cost')+ \
			self.quantity('Quantity')+ \
			self.cost('Cost')+'\n'
		return self._build(header, '') 
