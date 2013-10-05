#!/usr/bin/python

class AssemblyCost:
	def __init__(self):
		self.__component_costs=[]

	def add_cost(self, component_cost):
		self.__component_costs.append(component_cost)

	def add_costs(self, component_costs):
		self.__component_costs.extend(component_costs)
		
	def __amount(self):
		total=PartCost(0)
		for each in self.__component_costs:
			total=each.plus(total)
		return total

	def plus(self, part_cost):
		return part_cost.plus(self.__amount())

	def export(self, exporter):
		self.__amount().export(exporter)

	def __str__(self):
		return str(self.__amount())		
		

class PartCost:
	def __init__(self, value):
		self.__value=value

	def plus(self, part_cost):
		return part_cost.__add_to(self.__value)

	def __add_to(self, value):
		return PartCost(self.__value+value)

	def export(self, exporter):
		exporter.add_cost(self.__str__())		

	def __str__(self):
		return str(self.__value)
