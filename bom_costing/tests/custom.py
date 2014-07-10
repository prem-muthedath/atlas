#!/usr/bin/python

from . import test

from .. import export

class Custom(test.Test):
	#########################################################################################
	#### CUSTOMISED DISPLAYS -- PART ATTRIBUTES AND THEIR ORDER CHOSEN BY USER
	#########################################################################################

	def setUp(self):
		super(type(self), self).setUp()
		self.custom_part_fields=[export.base.PartSchema.NUMBER, export.base.PartSchema.LEVEL, export.base.PartSchema.COST]

	def test_text_output(self):
		print('\n')
		self.assertEquals(self.__expected_text_output(), export.exports.text_export(self.bom, self.custom_part_fields))
		
		print('\n\n'+'CUSTOMISED TEXT OUTPUT -- USER-SELECTED PART ATTRIBUTES AND PART-ATTRIBUTE ORDERING:\n')
		print export.exports.text_export(self.bom, self.custom_part_fields)

	def test_xml_output(self):
		print('\n')
		self.assertEquals(self.__expected_xml_output(), export.exports.xml_export(self.bom, self.custom_part_fields))
		
		print('\n\n'+'CUSTOMISED XML OUTPUT -- USER-SELECTED PART ATTRIBUTES AND PART-ATTRIBUTE ORDERING:\n')
		print export.exports.xml_export(self.bom, self.custom_part_fields), '\n'


	def __expected_text_output(self):
		return '\n'.join(['  Part Number       Level           Cost     ', 
							'     P-0001      1                  2000     ', 
							'     P-0002      1                   0       ', 
							'     P-0003        2                 0       ', 
							'     P-0004        2                 0       ', 
							'     P-0005        2                 0       ', 
							'     P-0006        2                 0       ', 
							'     P-0007        2                1400     ', 
							'     P-0008      1                   0       ', 
							'     P-0009        2                2000     ', 
							'     P-0010        2                 0       ', 
							'     P-0011        2                 0       ', 
							'     P-0012        2                 0       ', 
							'     P-0013        2                 0       ', 
							'     P-0014      1                   0       ', 
							'     P-0015        2                 0       ', 
							'     P-0016        2                 0       ', 
							'     P-0017        2                 0       ', 
							'     P-0018        2                 0       ', 
							'     P-0019        2                 0       ', 
							'     P-0020          3               0       ', 
							'     P-0021          3               0       ', 
							'     P-0022          3              2000     ', 
							'     P-0023        2                800      ', 
							'     P-0024      1                   5       ', 
							'     P-0025      1                   5       ', 
							'     P-0026      1                   0       ', 
							'     P-0027      1                   0       ', 
							''])

	def __expected_xml_output(self):
		return '\n'.join(['<?xml version="1.0" encoding="ISO-8859-1"?>', '<parts>', 
			'  <part><part_number>P-0001</part_number><level>1</level><cost>2000</cost></part>', 
			'  <part><part_number>P-0002</part_number><level>1</level><cost>0</cost></part>', 
			'  <part><part_number>P-0003</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0004</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0005</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0006</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0007</part_number><level>2</level><cost>1400</cost></part>', 
			'  <part><part_number>P-0008</part_number><level>1</level><cost>0</cost></part>', 
			'  <part><part_number>P-0009</part_number><level>2</level><cost>2000</cost></part>', 
			'  <part><part_number>P-0010</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0011</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0012</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0013</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0014</part_number><level>1</level><cost>0</cost></part>', 
			'  <part><part_number>P-0015</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0016</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0017</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0018</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0019</part_number><level>2</level><cost>0</cost></part>', 
			'  <part><part_number>P-0020</part_number><level>3</level><cost>0</cost></part>', 
			'  <part><part_number>P-0021</part_number><level>3</level><cost>0</cost></part>', 
			'  <part><part_number>P-0022</part_number><level>3</level><cost>2000</cost></part>', 
			'  <part><part_number>P-0023</part_number><level>2</level><cost>800</cost></part>', 
			'  <part><part_number>P-0024</part_number><level>1</level><cost>5</cost></part>', 
			'  <part><part_number>P-0025</part_number><level>1</level><cost>5</cost></part>', 
			'  <part><part_number>P-0026</part_number><level>1</level><cost>0</cost></part>', 
			'  <part><part_number>P-0027</part_number><level>1</level><cost>0</cost></part>', 
			'</parts>'])
