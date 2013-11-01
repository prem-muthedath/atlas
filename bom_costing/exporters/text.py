#!/usr/bin/python

from base import Exporter
from base import PartSchema

class TextExporter(Exporter):
	__FIELD_WIDTH=15

	def __init__(self):
		super(type(self), self).__init__()
		self.__headers=[]

	def build_field(self, name, value):
		self.__add_header(name)
		return self.__centered(value)

	def build_level(self, name, value):	
		self.__add_header(name)		
		indent=abs(int(value))*"  "
		return (indent+value).ljust(self.__FIELD_WIDTH)

	def __add_header(self, header):
		if len(self.__headers) < PartSchema.count():
			self.__headers.append(header)

	def __centered(self, value):
		return value.center(self.__FIELD_WIDTH)

	def _titled_part(self, part):
		return part+'\n'

	def _titled_content(self, content):
		return self.__title()+content
	
	def __title(self):
		return ''.join(self.__format(each) for each in self.__headers)+'\n'

	def __format(self, header):
		return self.__centered(self.__capitalize(header))

	def __capitalize(self, header):
		return ' '.join(each[:1].upper()+each[1:].lower() for each in header.split())
