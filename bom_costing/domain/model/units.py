#!/usr/bin/python

class Units:
	def __init__(self, quantity, unit_cost):
		self.__quantity=quantity
		self.__unit_cost=unit_cost

	def cost(self, cost):
		self.__quantity.cost(cost, self.__unit_cost)

	def add_to(self, part_builder):
		part_builder.add(self.__dict__.values())