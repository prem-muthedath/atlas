#!/usr/bin/python

class Cost:
	def __init__(self, value=0):
		self.__value=value

	def times(self, multiplier):
		return self.__class__(multiplier*self.__value)

	def add_costs(self, costs):
		start=self
		for each in costs:
			start=each.add(start)
		return start	

	def add(self, cost):
		return self.__class__(self.__value+cost.__value)

	def add_to(self, part_builder):
		part_builder.add_cost(self)

	def render(self, format):
		return format.cost(self.__str__())		

	def __str__(self):
		return str(self.__value)
