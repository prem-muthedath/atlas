#!/usr/bin/python

import collections
import string
import copy

class Exporter:
	def __init__(self, format):	
		self.__level=ExportLevel()
		self.__format=format

	def export(self, component):
		component.export(self)
		return self.__format.__str__()

	def add_bom(self, bom):
		self.__level.export_bom(bom, self)

	def add_part(self, part_data):
		part_data.append(self.__level)
		self.__format.export_part(part_data)


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


class Format(object):
	def __init__(self, part_builder):	
		self.__parts=[]
		self.__part_builder=part_builder

	def __str__(self):
		return self._titled_bom(self.__bom())

	def export_part(self, part_data):
		ordered_part=self.__part_builder.ordered_part(part_data)
		ordered_part.export(self)

	def add_part(self, part_export):
		self.__parts.append(''.join(part_export))

	def attribute(self, name, value):
		pass		

	def level(self, name, value):
		pass		

	def __bom(self):
		return ''.join(self._titled_part(each) for each in self.__parts)

	def _titled_part(self, part):
		pass

	def _titled_bom(self, bom):
		pass
		

class PartBuilder:
	def __init__(self, ordered_part):
		self.__part=ordered_part

	def ordered_part(self, part_data):	
		self.add(part_data)
		return copy.deepcopy(self.__part)

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


class OrderedPart:
	def __init__(self, fields=None):
		self.__attributes=collections.OrderedDict.fromkeys(PartSchema.order(fields))

	def add(self, field, value):
		if field in self.__fields():
			self.__attributes[field]=value

	def __fields(self):
		return self.__attributes.keys()

	def export(self, format):
		format.add_part([self.__export(field, format) for field in self.__fields()])

	def __export(self, field, format):
		return field.export(self.__attributes[field], format)


class Field:
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

	def export(self, value, format):
		if self==PartSchema.LEVEL:
			return format.level(self.__good_name(), value)
		return format.attribute(self.__good_name(), value)

	def __good_name(self):
		return ''.join(each if each not in string.punctuation else ' ' for each in list(self.__name))


class PartSchema:
	LEVEL=Field('level', 0)
	NUMBER=Field('part number', 1) 
	CODE=Field('source code', 2)
	UNIT_COST=Field('unit cost', 3)
	QUANTITY=Field('quantity', 4)
	COST=Field('cost', 5)

	@classmethod
	def fields(cls):
		return sorted([getattr(cls, each) for each in cls.__dict__.keys() 
				if each[:1]!='_' and not callable(getattr(cls, each))])

	@classmethod
	def order(cls, fields):
		if fields is None:
			return cls.fields()
		if set(fields)<=set(cls.fields()):	
			return fields
		raise ValueError("Invalid Part Field(s) Found.")