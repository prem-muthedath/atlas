#!/usr/bin/python

class TextViewFactory:
	def view(self):
		return BomTextView(BomPartTextView(LevelTextView(), PartTextView()))
		

class ComponentView(object):
	def _export(self, components):
		for each in components:
			each.export(self)

	def render(self):
		pass


class BomTextView(ComponentView):
	def __init__(self, bom_part_view):
		self.__bom_part_view=bom_part_view
		self.__output=[]

	def export_bom(self, bom_components):
		self.__bom_part_view.export_bom(bom_components, self)

	def export_part(self, part_data):
		self.__bom_part_view.export_part(part_data, self)

	def add_view(self, view):
		self.__output.append(view)

	def render(self): 
		return self.__header()+self.__render()	

	def __header(self):
		return self.__bom_part_view.header()

	def __render(self):
		return ''.join(self.__output)


class BomPartTextView():
	def __init__(self, level_view, part_view):
		self.__level_view=level_view
		self.__part_view=part_view

	def export_bom(self, bom_components, bom_view):
		self.__level_view.export_bom(bom_components, bom_view)

	def export_part(self, part_data, bom_view):
		self.__part_view._export(part_data)
		bom_view.add_view(self.render())

	def render(self): 
		return self.__format(
			self.__level_view.render(),
			self.__part_view.render())

	def header(self):
		return self.__format(
			self.__level_view.header(),
			self.__part_view.header())

	def __format(self, augend, addend):
		return augend+addend+'\n'


class LevelTextView:
	__COLUMN_WIDTH=13
	__HEADER='Level'

	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom_components, bom_view):
		self.__enter_bom()
		bom_view._export(bom_components)
		self.__exit_bom()

	def __enter_bom(self):
		self.__value+=1

	def __exit_bom(self):
		self.__value-=1

	def render(self):
		return self.__output().ljust(self.__COLUMN_WIDTH)

	def __output(self):
		indent=abs(self.__value)*"  "
		return indent+str(self.__value)

	def header(self):
		return self.__HEADER.center(self.__COLUMN_WIDTH)


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
