#!/usr/bin/python

from generic import View

class TextView(View):
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
		view=self.__class__()
		view.add_name('Part')
		view.add_code('Code')
		view.add_quantity('Quantity')
		view.add_cost('Cost')
		return view.__format_part()	

	def _footer(self):
		return ''