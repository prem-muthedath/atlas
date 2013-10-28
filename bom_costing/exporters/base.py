#!/usr/bin/python

from collections import OrderedDict

class Exporter:
	def __init__(self, builder):
		self.__builder=builder

	def export(self, bom):
		bom.export(ExportLevel(), self)
		return self.__builder.build()

	def export_part(self, part_data):
		self.__builder.add_part(part_data)


class Builder(object):
	def __init__(self):	
		self.__exports=[]

	def add_part(self, part_data):
		self.__exports.append(PartSchema().part(part_data, self))

	def part(self, mapped_data):
		pass

	def _part(self, prefix, mapped_data, suffix):
		return ''.join([prefix, ''.join(each.build(self) for each in mapped_data), suffix])

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

	def build(self):
		pass
			
	def _build(self, header, footer):
		return ''.join([header, ''.join(self.__exports), footer])


class ExportLevel:
	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom_components, exporter):
		for each in bom_components:
			each.export(self.__child(), exporter)

	def __child(self):
		return self.__class__(self.__value+1)

	def add_to(self, part_schema):
		part_schema.add_level(self)		

	def build(self, builder):
		return builder.level(str(self.__value))


class PartSchema:
	__FIELDS=('LEVEL', 'NUMBER', 'CODE', 'UNIT_COST', 'QUANTITY', 'COST')
	
	def __init__(self):
		self.__fields=OrderedDict((each, None) for each in self.__FIELDS)

	def part(self, part_data, builder):	
		self.add(part_data)
		return builder.part(self.__fields.values())

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