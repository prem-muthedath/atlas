#!/usr/bin/python

from collections import OrderedDict

class Exporter(object):
	def __init__(self):	
		self.__exports=[]

	def export(self, bom):
		bom.export(ExportLevel(), self)
		return self._build()

	def add_part(self, part_data):
		self.__exports.append(PartSchema().part(part_data, self))

	def part(self, ordered_data):
		return ''.join(each.export(self) for each in ordered_data)

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

	def unit_cost(self, cost):
		pass		

	def _build(self):
		return ''.join(self.__exports)

	def _format(self, prefix, content, suffix):
		return ''.join([prefix, content, suffix])


class ExportLevel:
	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom_components, exporter):
		for each in bom_components:
			each.export(self.__child(), exporter)

	def __child(self):
		return self.__class__(self.__value+1)

	def export_part(self, part_data, exporter):
		part_data.append(self)
		exporter.add_part(part_data)

	def add_to(self, part_schema):
		part_schema.add_level(self)		

	def export(self, exporter):
		return exporter.level(str(self.__value))


class PartSchema:
	__FIELDS=('LEVEL', 'NUMBER', 'CODE', 'UNIT_COST', 'QUANTITY', 'COST')
	
	def __init__(self):
		self.__fields=OrderedDict((each, None) for each in self.__FIELDS)

	def part(self, part_data, exporter):	
		self.add(part_data)
		return exporter.part(self.__fields.values())

	def add(self, part_data):
		for each in part_data:			
			each.add_to(self)		

	def add_level(self, level):
		self.__fields['LEVEL']=level

	def add_number(self, number):
		self.__fields['NUMBER']=number

	def add_code(self, code):
		self.__fields['CODE']=code

	def add_quantity(self, quantity):
		self.__fields['QUANTITY']=quantity

	def add_unit_cost(self, unit_cost):
		self.__fields['UNIT_COST']=unit_cost

	def add_cost(self, cost):
		self.__fields['COST']=cost