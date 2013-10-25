#!/usr/bin/python

from collections import OrderedDict
from StringIO import StringIO

class Exporter:
	def __init__(self, format):
		self.__exports=[]
		self.__format=format

	def export(self, bom):
		bom.export(ExportLevel(), self)
		return self.__package(self.__render())

	def export_part(self, part_data):
		part_export=self.__format.render_part(part_data)
		self.__exports.append(part_export)

	def __render(self):
		return self.__format.render(self)

	def	content(self):
		return ''.join(self.__exports)

	def __package(self, output):
		stream=StringIO()
		stream.writelines(output)
		stream.seek(0)
		return stream	


class Format(object):
	def render_part(self, part_data):
		return PartBuilder().build(part_data, self)

	def level(self, level):
		pass		

	def number(self, number):
		pass		

	def code(self, code):
		pass		

	def quantity(self, quantity):
		pass		

	def cost(self, cost):
		pass		

	def render(self, exporter):
		return self._header()+exporter.content()+self._footer()

	def header(self):
		return ''

	def _footer(self):
		return ''


class PartBuilder:
	__FIELDS=('LEVEL', 'NUMBER', 'CODE', 'QUANTITY', 'COST')
	
	def __init__(self):
		self.__part=OrderedDict((each, '') for each in self.__FIELDS)

	def build(self, part_data, format):	
		self.add(part_data)
		return ''.join(each.render(format) for each in self.__part.values())

	def add(self, part_data):
		for each in part_data:			
			each.add_to(self)		

	def add_level(self, level):
		self.__part['LEVEL']=level

	def add_number(self, number):
		self.__part['NUMBER']=number

	def add_code(self, code):
		self.__part['CODE']=code

	def add_quantity(self, quantity):
		self.__part['QUANTITY']=quantity

	def add_cost(self, cost):
		self.__part['COST']=cost


class ExportLevel:
	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom_components, exporter):
		for each in bom_components:
			each.export(self.__child(), exporter)

	def __child(self):
		return self.__class__(self.__value+1)

	def add_to(self, part_builder):
		part_builder.add_level(self)		

	def render(self, format):
		return format.level(str(self.__value))