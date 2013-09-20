#!/usr/bin/python

class Name:
	def __init__(self, name_string):
		self.__name=name_string

	def export(self, part_view):
		part_view.add_name(self.__name)