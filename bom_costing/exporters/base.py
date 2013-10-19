#!/usr/bin/python

from collections import OrderedDict

class Exporter:
	def __init__(self):
		self.__part_exporters=[]

	def export(self, bom):
		bom.export(ExportLevel(), self)		

	def export_part(self, part_data):
		self.__part_exporters.append(PartExporter(self))
		self.__part_exporters[-1].export_items(part_data)

	def level(self, level): 
		pass	

	def name(self, name): 
		pass

	def code(self, code): 
		pass

	def quantity(self, quantity): 
		pass

	def cost(self, cost): 
		pass

	def render_part(self, content_string): 
		pass

	def render(self):
		return self._header()+self._contents()+self._footer()

	def _header(self):
		return ''

	def _contents(self):
		return ''.join(each.render() for each in self.__part_exporters)

	def _footer(self):
		return ''


class PartExporter(object):
	def __init__(self, bom_exporter):
		self.__part=OrderedDict([('level', ''), ('name', ''), ('code', ''), ('quantity', ''), ('cost', '')]) 
		self.__bom_exporter=bom_exporter

	def export_items(self, items):	
		for each in items:			
			each.export(self)
	
	def add_level(self, level):
		self.__part['level']=self.__bom_exporter.level(level)

	def add_name(self, name):
		self.__part['name']=self.__bom_exporter.name(name)

	def add_code(self, code):
		self.__part['code']=self.__bom_exporter.code(code)

	def add_quantity(self, quantity):
		self.__part['quantity']=self.__bom_exporter.quantity(quantity)

	def add_cost(self, cost):
		self.__part['cost']=self.__bom_exporter.cost(cost)

	def render(self):
		return self.__bom_exporter.render_part(self.__contents())

	def __contents(self):
		return ''.join(self.__part.values())


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