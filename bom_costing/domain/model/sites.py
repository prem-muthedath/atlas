#!/usr/bin/python

class Sites:
	def __init__(self, source_code, bom):
		self.__source_code=source_code
		self.__bom=bom				

	def is_costed(self, part): 
		if self.__source_code.is_costed():
			return 1
		return self.__bom.costable(part, self.__source_code)

	def add_to(self, part_builder):
		part_builder.add(self.__dict__.values())