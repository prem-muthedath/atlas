#!/usr/bin/python

from base import PartExporter

class TextPartExporter(PartExporter):
	def add_level(self, level):
		self._super().add_level(self.__format_level(level))

	def __format_level(self, level):
		if self.__header_level(level):	
			return level.center(13)	
		return self.__indented_data_level(level).ljust(13)

	def __header_level(self, level):
		try:		
			int(level)
			return 0
		except ValueError:
			return 1

	def __indented_data_level(self, level):
		indent=abs(int(level))*"  "
		return indent+level
	
	def add_name(self, name):
		self._super().add_name(name.center(65))

	def add_code(self, code):
		self._super().add_code(code.center(10))

	def add_quantity(self, quantity):
		self._super().add_quantity(quantity.center(10))

	def add_cost(self, cost):
		self._super().add_cost(cost.center(10)+'\n')

	def header(self):
		self.add_name('Part')		
		self.add_level('Level')
		self.add_code('Code')
		self.add_quantity('Quantity')
		self.add_cost('Cost')
		return self._super().header()		
