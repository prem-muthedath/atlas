#!/usr/bin/python

class Name:
	def __init__(self, name_string):
		self.__name=name_string

	def export(self, view):
		view.add_name(self.__name)