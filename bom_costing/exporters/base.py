#!/usr/bin/python

class Exporter(object):
	def __init__(self):
		self.__export=Export()	
		self._current_part={'name':'', 'code':'', 'quantity':'', 'cost':''} 

	def export_bom(self, bom_components):
		self.__export.export_bom(bom_components, self)

	def export_part(self, part_data):
		self.export_items(part_data)
		self.__export.update(self)

	def export_items(self, items):
		for each in items:
			each.export(self)

	def add_name(self, name):
		self._current_part["name"]=name

	def add_code(self, code):
		self._current_part["code"]=code

	def add_quantity(self, quantity):
		self._current_part["quantity"]=quantity

	def add_cost(self, cost):
		self._current_part["cost"]=cost

	def part_export(self, level): 
		pass

	def render(self):
		return self.__export.render(self._layout())

	def _layout(self):
		return Layout()


class Export:
	def __init__(self):
		self.__contents=[]	
		self.__level=ExportLevel()	

	def export_bom(self, bom_components, exporter):
		self.__level.export_bom(bom_components, exporter)

	def update(self, exporter):
		self.__contents.append(self.__level.part_export(exporter))

	def render(self, layout):
		return layout.render(''.join(self.__contents))


class ExportLevel:
	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom_components, exporter):
		self.__enter_bom()
		exporter.export_items(bom_components)
		self.__exit_bom()

	def __enter_bom(self):
		self.__value+=1

	def __exit_bom(self):
		self.__value-=1

	def part_export(self, exporter):
		return exporter.part_export(self.__value)


class Layout:
	def __init__(self, header='', footer=''):
		self.__header=header
		self.__footer=footer

	def render(self, contents):
		return self.__header+contents+self.__footer
