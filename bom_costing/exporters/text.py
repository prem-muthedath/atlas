#!/usr/bin/python

from base import Exporter

class TextExporter(Exporter):
	__FIELD_WIDTH=15

	def __init__(self, part_builder):
		super(type(self), self).__init__(part_builder)
		self.__headers=[]

	def property(self, name, value):
		self.__add_header(name)
		return self.__centered(value)

	def level(self, name, value):	
		self.__add_header(name)		
		indent=abs(int(value))*"  "
		return (indent+value).ljust(self.__FIELD_WIDTH)

	def __add_header(self, header):
		header=self.__centered(self.__capitalize(header))
		if header not in self.__headers:
			self.__headers.append(header)

	def __capitalize(self, header):
		return ' '.join(each[:1].upper()+each[1:].lower() for each in header.split())

	def __centered(self, value):
		return value.center(self.__FIELD_WIDTH)

	def _titled_part(self, part):
		return part+'\n'

	def _titled_bom(self, bom):
		title=''.join(self.__headers)+'\n'
		return title+bom
