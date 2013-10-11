#!/usr/bin/python

from base import PartExporter
from base import Layout

class TextPartExporter(PartExporter):
	def render(self): 
		return self.__format_level()+self.__format_part()

	def __format_level(self):
		level=int(self._current_part['level'])
		indented_level=abs(level)*"  "+str(level)
		return indented_level.ljust(13)

	def __format_part(self):
			return self._current_part["name"].center(65)+ \
			self._current_part["code"].center(10)+ \
			self._current_part["quantity"].center(10)+ \
			self._current_part["cost"].center(10)+'\n'

	def layout(self, contents):
		return Layout(header=self.__header()).render(contents)

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