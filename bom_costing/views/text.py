#!/usr/bin/python

class ComponentView(object):
	def _export(self, components):
		for each in components:
			each.export(self)

	def render(self):
		pass


class Level:
	def __init__(self, value=-1):
		self.__value=value
		self.__HEADER='Level'

	def child(self):
		return self.__class__(self.__value+1)

	def parent(self):
		return self.__class__(self.__value-1)
	
	def render(self):
		return self.__format(self.__indented_string())

	def __indented_string(self):
		return abs(self.__value)*"    "+str(self.__value)

	def __format(self, value):
		return value.center(15)

	def header(self):
		return self.__format(self.__HEADER)


class BomTextView(ComponentView):
	def __init__(self):
		self.__level=Level()
		self.__output=''

	def export_bom(self, bom_components):
		self.__enter_child_bom()
		self._export(bom_components)
		self.__exit_child_bom()

	def __enter_child_bom(self):
		self.__level=self.__level.child()

	def __exit_child_bom(self):
		self.__level=self.__level.parent()

	def export_part(self, part_data):
		self._part_view().export_part(part_data, self)

	def _part_view(self):
		return PartTextView()

	def exported(self, part_view):
		self.__output+=self.__level.render()+part_view.render()

	def render(self): 
		return ''.join([self.__header(), self.__output])		

	def __header(self):
		return ''.join([self.__level.header(), self._part_view().header()])	


class PartTextView(ComponentView):
	def __init__(self):
		self.__data={'name':'', 'code':'', 'quantity':'', 'cost':''} 

	def add_name(self, name):
		self.__data["name"]=name

	def add_code(self, code):
		self.__data["code"]=code

	def add_quantity(self, quantity):
		self.__data["quantity"]=quantity

	def add_cost(self, cost):
		self.__data["cost"]=cost

	def export_part(self, part_data, bom_view):
		self._export(part_data)
		bom_view.exported(self)

	def render(self): 
		return self.__data["name"].center(65)+ \
			self.__data["code"].center(10)+ \
			self.__data["quantity"].center(10)+ \
			self.__data["cost"].center(10)+'\n'

	def header(self):
		return self.__header_view().render()

	def __header_view(self):
		part_view=self.__class__()
		part_view.add_name('Part')
		part_view.add_code('Code')
		part_view.add_quantity('Quantity')
		part_view.add_cost('Cost')
		return part_view				
