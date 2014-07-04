#!/usr/bin/python

from collections import OrderedDict
import string

class Exporter(object):
	def __init__(self, part_builder):	
		self.__parts=[]
		self.__level=ExportLevel()
		self.__part_builder=part_builder

	def export(self, component):
		component.export(self)
		return self._titled_bom(self.__bom())

	def add_bom(self, bom):
		self.__level.export_bom(bom, self)

	def add_part(self, part_data):
		part_data.append(self.__level)
		self.__parts.append(self.__part_builder.part(part_data, self))

	def property(self, name, value):
		pass		

	def level(self, name, value):
		pass		

	def __bom(self):
		return ''.join(self._titled_part(each) for each in self.__parts)

	def _titled_part(self, part):
		pass

	def _titled_bom(self, bom):
		pass
		

class ExportLevel:
	def __init__(self, value=-1):
		self.__value=value		

	def export_bom(self, bom, exporter):
		self.__enter_bom()
		bom.export_children(exporter)
		self.__exit_bom()

	def __enter_bom(self):
		self.__value+=1

	def __exit_bom(self):
		self.__value-=1

	def add_to(self, part_builder):
		part_builder.add_level(self.__data())		

	def __data(self):
		return str(self.__value)


class PartBuilder:
	def __init__(self, part):
		self.__part=part

	def part(self, part_data, exporter):	
		self.add(part_data)
		return self.__part.format(exporter)

	def add(self, part_data):
		for each in part_data:			
			each.add_to(self)		

	def add_level(self, level):
		self.__part.add(PartSchema.LEVEL, level)

	def add_number(self, number):
		self.__part.add(PartSchema.NUMBER, number)

	def add_code(self, code):
		self.__part.add(PartSchema.CODE, code)

	def add_quantity(self, quantity):
		self.__part.add(PartSchema.QUANTITY, quantity)

	def add_unit_cost(self, unit_cost):
		self.__part.add(PartSchema.UNIT_COST, unit_cost)

	def add_cost(self, cost):
		self.__part.add(PartSchema.COST, cost)


class Part:
	def __init__(self, attributes):
		self.__part=OrderedDict((attribute, None) for attribute in attributes)

	def add(self, attribute, value):
		if attribute in self.__part_attributes():
			self.__part[attribute]=value

	def __part_attributes(self):
		return self.__part.keys()

	def format(self, exporter):
		return ''.join(self.__export(attribute, exporter) for attribute in self.__part_attributes())

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
		if self==PartSchema.LEVEL:
			return exporter.level(self.__good_name(), value)
		return exporter.property(self.__good_name(), value)

	def __good_name(self):
		return ''.join(each if each not in string.punctuation else ' ' for each in list(self.__name))


class PartSchema:
	LEVEL=Attribute('level', 0)
	NUMBER=Attribute('part number', 1) 
	CODE=Attribute('source code', 2)
	UNIT_COST=Attribute('unit cost', 3)
	QUANTITY=Attribute('quantity', 4)
	COST=Attribute('cost', 5)

	@classmethod
	def attributes(cls):
		return sorted([getattr(cls, each) for each in cls.__dict__.keys() 
				if each[:1]!='_' and not callable(getattr(cls, each))])

	@classmethod
	def size(cls):
		return len(cls.attributes())

	@classmethod
	def part(cls, attributes=None):
		if attributes is None:
			return Part(cls.attributes())
		if set(attributes)<=set(cls.attributes()):	
			return Part(attributes)
		raise ValueError("Invalid Part Attribute(s) Found.")