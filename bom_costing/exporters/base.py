#!/usr/bin/python

from collections import OrderedDict
import string

class Exporter(object):
	def __init__(self):	
		self.__parts=[]

	def export(self, bom):
		bom.export(ExportLevel(), self)
		return self._titled_bom(self.__bom())

	def add_part(self, part_data):
		self.__parts.append(PartBuilder().part(part_data, self))

	def property(self, name, value):
		pass		

	def level(self, name, value):
		pass		

	def __bom(self):
		return ''.join(self._titled_part(each) for each in self.__parts)

	def _titled_bom(self, bom):
		pass

	def _titled_part(self, part):
		pass


class ExportLevel:
	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom_components, exporter):
		for each in bom_components:
			each.export(self.__child(), exporter)

	def __child(self):
		return self.__class__(self.__value+1)

	def export_part(self, part_data, exporter):
		part_data.append(self)
		exporter.add_part(part_data)

	def add_to(self, part_builder):
		part_builder.add_level(self)		

	def export(self, name, exporter):
		return exporter.level(name, str(self.__value))


class PartBuilder:
	def __init__(self):
		self.__part=OrderedDict((attribute, None) for attribute in PartSchema.attributes())

	def part(self, part_data, exporter):	
		self.add(part_data)
		return ''.join(self.__export(attribute, exporter) for attribute in self.__part_attributes())

	def add(self, part_data):
		for each in part_data:			
			each.add_to(self)		

	def add_level(self, level):
		self.__part[PartSchema.LEVEL]=level

	def add_number(self, number):
		self.__part[PartSchema.NUMBER]=number

	def add_code(self, code):
		self.__part[PartSchema.CODE]=code

	def add_quantity(self, quantity):
		self.__part[PartSchema.QUANTITY]=quantity

	def add_unit_cost(self, unit_cost):
		self.__part[PartSchema.UNIT_COST]=unit_cost

	def add_cost(self, cost):
		self.__part[PartSchema.COST]=cost

	def __part_attributes(self):
		return self.__part.keys()

	def __export(self, attribute, exporter):
		return attribute.export(self.__part[attribute], exporter)


class Attribute:
	def __init__(self, name, order):
		self.__name=name
		self.__order=order

	def __eq__(self, another):
		return (type(another) is type(self) and self.__dict__==another.__dict__)

	def __cmp__(self, another):
		if type(another) is type(self): 
			return cmp(self.__order, another.__order)
		raise ValueError('Can not compare -- Type mismatch!')

	def __hash__(self):
		return hash(self.__name)

	def export(self, value, exporter):
		return value.export(self.__good_name(), exporter)

	def __good_name(self):
		return ''.join(each if each not in string.punctuation else ' ' for each in list(self.__name))


class PartSchema:
	LEVEL=Attribute('level', 0)
	NUMBER=Attribute('number', 1) 
	CODE=Attribute('code', 2)
	UNIT_COST=Attribute('unit cost', 3)
	QUANTITY=Attribute('quantity', 4)
	COST=Attribute('cost', 5)

	@classmethod
	def attributes(cls):
		return sorted([getattr(cls, each) for each in cls.__dict__.keys() 
				if each[:1]!='_' and not callable(getattr(cls, each))])

	@classmethod
	def count(cls):
		return len(cls.attributes())