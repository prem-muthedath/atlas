#!/usr/bin/python

import base

class TextFormat(base.Format):
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


class XmlFormat(base.Format):
	def __init__(self, part_builder):
		super(type(self), self).__init__(part_builder)
	
	def property(self, name, value):
		return '<'+self.__format(name)+'>'+value+'</'+self.__format(name)+'>'

	def __format(self, name):
		return '_'.join(name.split())

	def level(self, name, value):
		return self.property(name, value)
		
	def _titled_part(self, part):
		indent='  '
		return indent+'<part>'+part+'</part>'+'\n'

	def _titled_bom(self, bom):
		return '<?xml version="1.0" encoding="ISO-8859-1"?>'+'\n'+ \
				'<parts>'+'\n'+bom+'</parts>'
