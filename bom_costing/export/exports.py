#!/usr/bin/python

import base
import formats

def text_export(bom, part_schema=None):
	return __exporter(formats.TextFormat, part_schema).export(bom)

def xml_export(bom, part_schema=None):
	return __exporter(formats.XmlFormat, part_schema).export(bom)

def __exporter(format, part_schema):
	return base.Exporter(format(__part_builder(part_schema)))

def __part_builder(part_schema):
		return base.PartBuilder(base.OrderedPart(part_schema))
