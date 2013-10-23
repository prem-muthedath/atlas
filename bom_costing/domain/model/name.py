#!/usr/bin/python

class Name:
	def __init__(self, name_string):
		self.__name=name_string

	def export(self, part_exporter):
		part_exporter.add_name(self.__name)
