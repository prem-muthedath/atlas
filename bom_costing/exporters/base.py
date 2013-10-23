#!/usr/bin/python

from collections import OrderedDict

class Exporter:
	def __init__(self, format):
		self.__exporters=[]
		self.__format=format

	def export(self, bom):
		bom.export(ExportLevel(), self)
		return self.render()

	def export_part(self, part_data):
		self.__exporters.append(PartExporter())
		self.__exporters[-1].export_items(part_data)

	def render(self):
		return self.__format.render(self.__contents())

	def __contents(self):
		return ''.join(each.render(self.__format) for each in self.__exporters)


class Format(object):
	def part_string(self, level, name, code, quantity, cost):
		return self._level(level)+ \
			self._name(name)+ \
			self._code(code)+ \
			self._quantity(quantity)+ \
			self._cost(cost)		

	def _level(self, level):
		pass		

	def _name(self, name):
		pass		

	def _code(self, code):
		pass		

	def _quantity(self, quantity):
		pass		

	def _cost(self, cost):
		pass		

	def render(self, exports):
		return self._header()+exports+self._footer()

	def _header(self):
		return ''

	def _footer(self):
		return ''


class PartExporter:
	def __init__(self):
		self.__part=OrderedDict([('level', ''), ('name', ''), ('code', ''), ('quantity', ''), ('cost', '')]) 		

	def export_items(self, items):	
		for each in items:			
			each.export(self)

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

	def render(self, format):
		return format.part_string(*self.__part.values())


class ExportLevel:
	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom_components, exporter):
		for each in bom_components:
			each.export(self.__child(), exporter)

	def __child(self):
		return self.__class__(self.__value+1)

	def export(self, part_exporter):
		return part_exporter.add_level(str(self.__value))