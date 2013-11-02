#!/usr/bin/python

from base import Exporter

class XmlExporter(Exporter):
	def property(self, name, value):
		return '<'+self.__format(name)+'>'+value+'</'+self.__format(name)+'>'

	def __format(self, name):
		return '_'.join(name.split())

	def level(self, name, value):
		return self.property(name, value)
		
	def _titled_part(self, part):
		return '  '+'<part>'+part+'</part>'+'\n'

	def _titled_bom(self, bom):
		return '<?xml version="1.0" encoding="ISO-8859-1"?>'+'\n'+ \
				'<parts>'+'\n'+bom+'</parts>'
