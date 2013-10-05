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

	def build(self):
		return str(self.__export)


class Export:
	def __init__(self):
		self.__contents=[]	
		self.__level=ExportLevel()	

	def export_bom(self, bom_components, exporter):
		self.__level.export_bom(bom_components, exporter)

	def update(self, exporter):
		self.__contents.append(self.__level.part_export(exporter))

	def __str__(self):
		return ''.join(self.__contents)


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


class TextExporter(Exporter):
	def part_export(self, level): 
		return self.__format_level(level)+self.__format_part()

	def __format_level(self, level):
		indented_level=abs(level)*"  "+str(level)
		return indented_level.ljust(13)

	def __format_part(self):
			return self._current_part["name"].center(65)+ \
			self._current_part["code"].center(10)+ \
			self._current_part["quantity"].center(10)+ \
			self._current_part["cost"].center(10)+'\n'

	def build(self):
		return self.__header()+super(type(self), self).build()

	def __header(self):
		return self.__level_header()+self.__part_header()

	def __level_header(self):
		return 'Level'.center(13)		

	def __part_header(self):
		exporter=self.__class__()
		exporter.add_name('Part')
		exporter.add_code('Code')
		exporter.add_quantity('Quantity')
		exporter.add_cost('Cost')
		return exporter.__format_part()	