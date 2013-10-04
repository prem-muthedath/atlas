#!/usr/bin/python

from layouts import TextLayout

class ViewFactory:
	def text_view(self):
		return View(TextLayout())
		

class View:
	def __init__(self, layout):
		self.__contents=[]	
		self.__level=ViewLevel()
		self.__layout=layout	

	def render(self, bom):
		bom.export(self)
		return self.__layout.render_view(self)

	def export_bom(self, bom_components):
		self.__level.export_bom(bom_components, self)

	def export_part(self, part_data):
		self.__layout.export(part_data)
		self.__update()

	def export(self, items):
		self.__layout.export(items, self)

	def __update(self):
		self.__contents.append(self.__level.render_part(self.__layout))

	def __str__(self):
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

	def render_part(self, layout):
		return layout.render_part(self.__value)
