#!/usr/bin/python

class SourceCode:
	def __init__(self, code):
		self.__code=code

	def is_costed(self):  
		return self.__code=='12'

	def costable(self):
		return self.__code=='1'

	def export(self, view_part):
		view_part.add_code(self.__code)	
