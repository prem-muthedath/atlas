#!/usr/bin/python

from base import Format

class TextFormat(Format):
	def level(self, level):
		indent=abs(int(level))*"  "
		return (indent+level).ljust(13)

	def number(self, number):
		return number.center(10)

	def code(self, code):
		return code.center(10)

	def quantity(self, quantity):
		return quantity.center(10)

	def cost(self, cost):
		return cost.center(10)

	def render_part(self, part_data):		
		return super(type(self), self).render_part(part_data)+'\n'

	def _header(self):
		return 'Level'.center(13)+ \
			self.number('Part')+ \
			self.code('Code')+ \
			self.quantity('Quantity')+ \
			self.cost('Cost')+'\n'
