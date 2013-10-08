#!/usr/bin/python

from base import Exporter
from base import Layout

class TextExporter(Exporter):
	def part_export(self, level): 
		return self.__format_level(level)+self.__format_part()

	def __format_level(self, level):
		indented_level=abs(level)*"  "+str(level)
		return indented_level.ljust(13)

	def __format_part(self):
			return self._current_part["name"].center(65)+ \
			self._current_part["code"].center(10)+ \
			self._current_part["quantity"].center(10)+ \
			self._current_part["cost"].center(10)+'\n'

	def _layout(self):
		return Layout(header=self.__header())

	def __header(self):
		return self.__level_header()+self.__part_header()

	def __level_header(self):
		return 'Level'.center(13)		

	def __part_header(self):
		exporter=self.__class__()
		exporter.add_name('Part')
		exporter.add_code('Code')
		exporter.add_quantity('Quantity')
		exporter.add_cost('Cost')
		return exporter.__format_part()	