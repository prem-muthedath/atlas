#!/usr/bin/python

class View:
	def __init__(self):
		self._current_part={'name':'', 'code':'', 'quantity':'', 'cost':''} 
		self.__contents=ViewContents()	

	def export_bom(self, bom_components):
		self.__contents.export_bom(bom_components, self)

	def export_part(self, part_data):
		self.export(part_data)
		self.__contents.add_part(self)

	def export(self, items):
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

	def render_part(self, level): 
		pass

	def render(self):
		return self._header()+self.__contents.render()+self._footer()

	def _header(self):
		pass

	def _footer(self):
		pass


class ViewContents:
	def __init__(self):
		self.__contents=[]	
		self.__level=ViewLevel()		

	def export_bom(self, bom_components, view):
		self.__level.export_bom(bom_components, view)

	def add_part(self, view):
		self.__contents.append(self.__level.render_part(view))

	def render(self):
		return ''.join(self.__contents)


class ViewLevel:
	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom_components, view):
		self.__enter_bom()
		view.export(bom_components)
		self.__exit_bom()

	def __enter_bom(self):
		self.__value+=1

	def __exit_bom(self):
		self.__value-=1

	def render_part(self, view):
		return view.render_part(self.__value)
