#!/usr/bin/python

from collections import OrderedDict

class Exporter(object):
	def __init__(self, format):
		self.__format=format	
		self.__exports=[]

	def export(self, bom):
		bom.export(ExportLevel(), self)		
		return self.__layout()

	def export_part(self, part_data):
		self.__exports.append(self.__part_exporter().export(part_data))

	def __part_exporter(self):
		return PartExporter(self.__format)

	def __layout(self):
		total=self.__header()
		for each in self.__exports:
			total=total.add(each)
		return total

	def __header(self):
		return Export(self.__format.header())


class PartExporter(object):
	def __init__(self, format):
		self.__part=OrderedDict([('level', ''), ('name', ''), ('code', ''), ('quantity', ''), ('cost', '')]) 
		self.__format=format

	def export(self, part_data):
		self.export_items(part_data)
		return Export(''.join(self.__part.values()))				

	def export_items(self, items):	
		for each in items:			
			each.export(self)
	
	def add_level(self, level):
		self.__part['level']=self.__format.level(level)

	def add_name(self, name):
		self.__part['name']=self.__format.name(name)

	def add_code(self, code):
		self.__part['code']=self.__format.code(code)

	def add_quantity(self, quantity):
		self.__part['quantity']=self.__format.quantity(quantity)

	def add_cost(self, cost):
		self.__part['cost']=self.__format.cost(cost)


class Export:
	def __init__(self, data=''):
		self.__data=data

	def add(self, export):
		return export.add_to(self.__data)	

	def add_to(self, data):
		return Export(data+self.__data)

	def __str__(self):
		return str(self.__data)


class ExportLevel:
	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom_components, exporter):
		for each in bom_components:
			each.export(self.__child(), exporter)

	def __child(self):
		return self.__class__(self.__value+1)

	def export(self, exporter):
		exporter.add_level(str(self.__value))