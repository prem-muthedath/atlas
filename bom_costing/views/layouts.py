#!/usr/bin/python

class Layout:
	def __init__(self):
		self._current_part={'name':'', 'code':'', 'quantity':'', 'cost':''} 

	def export(self, items, destination=None):
		if destination is None: 
			destination=self
		for each in items:
			each.export(destination)

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

	def render_view(self, view):
		return self._header()+view.__str__()+self._footer()

	def _header(self):
		pass

	def _footer(self):
		pass


class TextLayout(Layout):
	def render_part(self, level): 
		return self.__format_level(level)+self.__format_part()

	def __format_level(self, level):
		indented_level=abs(level)*"  "+str(level)
		return indented_level.ljust(13)

	def __format_part(self):
			return self._current_part["name"].center(65)+ \
			self._current_part["code"].center(10)+ \
			self._current_part["quantity"].center(10)+ \
			self._current_part["cost"].center(10)+'\n'

	def _header(self):
		return self.__level_header()+self.__part_header()

	def __level_header(self):
		return 'Level'.center(13)		

	def __part_header(self):
		layout=self.__class__()
		layout.add_name('Part')
		layout.add_code('Code')
		layout.add_quantity('Quantity')
		layout.add_cost('Cost')
		return layout.__format_part()	

	def _footer(self):
		return ''