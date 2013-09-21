#!/usr/bin/python

class ComponentView(object):
	def _export(self, components):
		for each in components:
			each.export(self)
	
	def render(self):
		pass
					

class BomTextView(ComponentView):
	def __init__(self, level=-1):
		self.__level=level
		self.__component_views=ComponentViews()

	def export_bom(self, bom_components):
		self.__export_items(self._child_bom_view(), bom_components)

	def _child_bom_view(self):
		return BomTextView(self.__child_level())

	def __child_level(self):
		return self.__level+1

	def export_part(self, part_data):
		self.__export_items(self._part_view(), part_data)

	def _part_view(self):
		return PartTextView()

	def __export_items(self, view, items):
		self.__component_views.add(view)
		view._export(items)

	def render(self, level=None): 
		return self.__header()+self.__component_views.render(self.__level)

	def __header(self):
		if(self.__top_level()): 
			return PartTextView.header()
		return ''

	def __top_level(self):
		return self.__level==0


class ComponentViews:
	def __init__(self):
		self.__views=[]

	def add(self, component_view):
		self.__views.append(component_view)

	def render(self, level): 
		result=[]
		for each in self.__views:
			result.append(each.render(level))
		return "".join(result) 		


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

	def render(self, level): 
		return self.__format_level_string(level)+self.__format_part_string()+"\n"
	
	def __format_part_string(self):
		return self.__data["name"].center(65)+ \
			self.__data["code"].center(15)+ \
			self.__data["quantity"].center(10)+ \
			self.__data["cost"].center(10)

	def __format_level_string(self, level):
		return (self.__indent(level)+str(level)).ljust(15)

	def __indent(self, level):
		return abs(level)*"    "

	@classmethod
	def header(cls):
		return 'Level'.center(15)+'Part'.center(65)+ \
			'Code'.center(15)+'Quantity'.center(10)+ \
			'Cost'.center(10)+'\n'




