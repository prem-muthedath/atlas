#!/usr/bin/python

from base import Exporter

class TextExporter(Exporter):
	def level(self, level):
		indent=abs(int(level))*"  "
		return (indent+level).ljust(13)

	def name(self, name):
		return name.center(65)

	def code(self, code):
		return code.center(10)

	def quantity(self, quantity):
		return quantity.center(10)

	def cost(self, cost):
		return cost.center(10)

	def render_part(self, content_string):
		return content_string+'\n'

	def _header(self):
		return 'Level'.center(13)+ \
			self.name('Part')+ \
			self.code('Code')+ \
			self.quantity('Quantity')+ \
			self.cost('Cost')+'\n'
