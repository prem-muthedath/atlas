#!/usr/bin/python

from collections import OrderedDict

class Exporter(object):
	def __init__(self, part_exporter_type):
		self.__part_exporter_type=part_exporter_type	
		self.__exports=[]

	def export(self, bom):
		bom.export(ExportLevel(), self)		
		return self.__layout()

	def export_part(self, part_data):
		self.__exports.append(self.__part_exporter().export(part_data))

	def __part_exporter(self):
		return self.__part_exporter_type()	

	def __layout(self):
		total=self.__header()
		for each in self.__exports:
			total=total.add(each)
		return total

	def __header(self):
		return self.__part_exporter().header()


class PartExporter(object):
	def __init__(self):
		self.__part=OrderedDict([('level', ''), ('name', ''), ('code', ''), ('quantity', ''), ('cost', '')]) 

	def export(self, part_data):
		self.export_items(part_data)
		return self.__layout()

	def export_items(self, items):	
		for each in items:			
			each.export(self)

	def __layout(self):
		return Export(''.join(self.__part.values()))

	def add_level(self, level):
		self.__part['level']=level

	def add_name(self, name):
		self.__part['name']=name

	def add_code(self, code):
		self.__part['code']=code

	def add_quantity(self, quantity):
		self.__part['quantity']=quantity

	def add_cost(self, cost):
		self.__part['cost']=cost

	def _super(self):
		return super(type(self), self)

	def header(self):
		return self.__layout()		


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