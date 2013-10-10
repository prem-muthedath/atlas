#!/usr/bin/python

from collections import OrderedDict

class Exporter(object):
	def __init__(self):
		self._current_part={'name':'', 'code':'', 'quantity':'', 'cost':''} 
		self.__export=Export()

	def render(self, bom):
		bom.export(ExportLevel(), self)		
		return self.__export.render(self._layout())

	def export_part(self, part_data):
		self.export_items(part_data)
		self.__export.add(self._part_export())

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

	def _part_export(self):
		pass		

	def _layout(self):
		return Layout()


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


class Export:
	def __init__(self):
		self.__contents=[]	

	def add(self, part_export):
		self.__contents.append(part_export)

	def render(self, layout):
		return layout.render(''.join(self.__contents))


class Layout:
	def __init__(self, header='', footer=''):
		self.__header=header
		self.__footer=footer

	def render(self, contents):
		return self.__header+contents+self.__footer

