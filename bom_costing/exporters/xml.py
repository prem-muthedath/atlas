#!/usr/bin/python

from base import Exporter

class XmlExporter(Exporter):
	def level(self, level):
		return self.__field('level', level)

	def number(self, number):
		return self.__field('number', number)

	def code(self, code):
		return self.__field('code', code)

	def quantity(self, quantity):
		return self.__field('quantity', quantity)

	def unit_cost(self, unit_cost):
		return self.__field('unit_cost', unit_cost)

	def cost(self, cost):
		return self.__field('cost', cost)

	def __field(self, name, value):
		return self.__indent(2)+'<'+name+'>'+value+'</'+name+'>'+'\n'

	def part(self, mapped_data):
		part=super(type(self), self).part(mapped_data)
		prefix=self.__indent(1)+'<part>'+'\n'
		suffix=self.__indent(1)+'</part>'+'\n'
		return self._format(prefix, part, suffix)

	def __indent(self, tabs):
		TAB='  '
		return tabs*TAB

	def _build(self):
		content=super(type(self), self)._build()		
		header='<?xml version="1.0" encoding="ISO-8859-1"?>'+'\n'+'<parts>'+'\n'
		footer='</parts>'
		return self._format(header, content, footer)
