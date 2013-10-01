#!/usr/bin/python

class ComponentView(object):
	def _export(self, components):
		for each in components:
			each.export(self)

	def render(self):
		pass


class BomView(ComponentView):
	def __init__(self, bom_part_view):
		self.__bom_part_view=bom_part_view
		self.__output=[self.__header()]

	def export_bom(self, bom_components):
		self.__bom_part_view.export_bom(bom_components, self)

	def export_part(self, part_data):
		self.__bom_part_view.export_part(part_data, self)

	def add_view(self, view):
		self.__output.append(view)

	def render(self): 
		return ''.join(self.__output)		

	def __header(self):
		return self.__bom_part_view.header()


class BomPartView():
	def __init__(self, level_view, part_view):
		self.__level_view=level_view
		self.__part_view=part_view

	def export_bom(self, bom_components, bom_view):
		self.__level_view.export_bom(bom_components, bom_view)

	def export_part(self, part_data, bom_view):
		self.__part_view._export(part_data)
		bom_view.add_view(self.render())

	def render(self): 
		return self.__level_view.render()+ \
			self.__part_view.render() +'\n'

	def header(self):
		return self.__level_view.header()+ \
			self.__part_view.header()+'\n'


class LevelTextView:
	def __init__(self, value=-1):
		self.__value=value
		self.__HEADER='Level'

	def export_bom(self, bom_components, bom_view):
		self.__enter_bom()
		bom_view._export(bom_components)
		self.__exit_bom()

	def __enter_bom(self):
		self.__value+=1

	def __exit_bom(self):
		self.__value-=1

	def render(self):
		return self.__format(self.__indented_string())

	def __indented_string(self):
		return abs(self.__value)*"    "+str(self.__value)

	def __format(self, value):
		return value.center(15)

	def header(self):
		return self.__format(self.__HEADER)


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

	def render(self): 
		return self.__data["name"].center(65)+ \
			self.__data["code"].center(10)+ \
			self.__data["quantity"].center(10)+ \
			self.__data["cost"].center(10)

	def header(self):
		return self.__header_view().render()

	def __header_view(self):
		part_view=self.__class__()
		part_view.add_name('Part')
		part_view.add_code('Code')
		part_view.add_quantity('Quantity')
		part_view.add_cost('Cost')
		return part_view				
