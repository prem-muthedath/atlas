#!/usr/bin/python

class Exporter(object):
	def __init__(self, part_exporter_type):
		self.__part_exporter_type=part_exporter_type	
		self.__part_exporters=[]

	def render(self, bom):
		bom.export(ExportLevel(), self)		
		return self.__part_exporter_type().layout(self.__content())

	def export_part(self, part_data):
		self.__part_exporters.append(self.__part_exporter_type())
		self.__part_exporters[-1].export_items(part_data)

	def __content(self):
		rendered_contents=[]
		for each in self.__part_exporters:
			rendered_contents.append(each.render())
		return ''.join(rendered_contents)							


class PartExporter(object):
	def __init__(self):
		self._current_part={'level:'', name':'', 'code':'', 'quantity':'', 'cost':''} 

	def export_items(self, items):	
		for each in items:			
			each.export(self)

	def add_level(self, level):
		self._current_part['level']=level

	def add_name(self, name):
		self._current_part["name"]=name

	def add_code(self, code):
		self._current_part["code"]=code

	def add_quantity(self, quantity):
		self._current_part["quantity"]=quantity

	def add_cost(self, cost):
		self._current_part["cost"]=cost

	def _render(self):
		pass	

	def layout(self, contents):
		return Layout().render(contents)				


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


class Layout:
	def __init__(self, header='', footer=''):
		self.__header=header
		self.__footer=footer

	def render(self, content):
		return self.__header+content+self.__footer
