#!/usr/bin/python

class SourceCode:
	def __init__(self, code):
		self.__code=code

	def is_costed(self):  
		return self.__code=='12'

	def costable(self):
		return self.__code=='1'

	def add_to(self, part_schema):
		part_schema.add_code(self)

	def build(self, builder):
		return builder.code(self.__code)	
