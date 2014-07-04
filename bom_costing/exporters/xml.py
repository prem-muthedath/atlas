#!/usr/bin/python

from base import Exporter

class XmlExporter(Exporter):
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
