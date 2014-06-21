#!/usr/bin/python

from model.components import Bom
from model.components import Part
from model.number import Number
from model.source_code import SourceCode
from model.sites import Sites
from model.quantity import Quantity
from model.costs import UnitCost
from model.units import Units

class BomBuilder():
	def __init__(self):
		self.__parents=[Bom()]
		self.__parent_level=0

	def add_item(self, level, number, code, cost, quantity):
		self.__new_level(level)
		self.__add(number, code, cost, quantity, self.__parent())
		self.__new_parents()

	def __new_level(self, level):
		self.__parent_level=level

	def __add(self, number, code, cost, quantity, bom):
		sites=Sites(SourceCode(code), bom)
		units=Units(Quantity(quantity), UnitCost(cost))
		part=Part(Number(number), sites, units)
		bom.add(part)

	def __parent(self):
		if(self.__new_bom()): self.__create()
		return self.__parents[self.__parent_level]

	def __new_bom(self):
		return self.__parent_level==self.__previous_parent_level()+1

	def __previous_parent_level(self):
		return len(self.__parents)-1

	def __create(self):
		self.__parents.append(Bom())
		self.__parents[self.__parent_level-1].add(self.__parents[self.__parent_level])
	
	def __new_parents(self):
		self.__parents=self.__parents[0:self.__parent_level+1]

	def build(self):
		return self.__parents[0]
