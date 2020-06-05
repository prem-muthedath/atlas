#!/usr/bin/python

class DuplicateError(Exception):
	def __init__(self, value):
		self.value=value

	def __str__(self):
		return str(self.value)