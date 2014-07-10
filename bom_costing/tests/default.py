#!/usr/bin/python

from . import base

from .. import export

class Default(base.Test):
	#####################################################################################################
	#### DEFAULT DISPLAYS -- INCLUDES ALL PART ATTRIBUTES, IN THE ORDER DEFINED IN export.base.PartSchema
	#####################################################################################################

	def test_text_output(self):
		print('\n')
		self.assertEquals(self.__expected_text_output(), export.exports.text_export(self.bom))
		
		print('\n\n'+'DEFAULT TEXT OUTPUT -- INCLUDES ALL PART ATTRIBUTES IN THE DEFAULT ORDER:\n')
		print export.exports.text_export(self.bom)

	def test_xml_output(self):
		print('\n')
		self.assertEquals(self.__expected_xml_output(), export.exports.xml_export(self.bom))
		
		print('\n\n'+'DEFAULT XML OUTPUT -- INCLUDES ALL PART ATTRIBUTES IN THE DEFAULT ORDER:\n')
		print export.exports.xml_export(self.bom), '\n'

	def __expected_text_output(self):
		return '\n'.join(['     Level       Part Number    Source Code     Unit Cost       Quantity         Cost     ', 
					'  1                 P-0001           1             1000            2             2000     ', 
					'  1                 P-0002           1             1000            2              0       ', 
					'    2               P-0003          120            2000            2              0       ', 
					'    2               P-0004           11            1500            1              0       ', 
					'    2               P-0005           78            100             1              0       ', 
					'    2               P-0006          007            700             2              0       ', 
					'    2               P-0007          007            700             2             1400     ', 
					'  1                 P-0008           13            1000            1              0       ', 
					'    2               P-0009           12            2000            1             2000     ', 
					'    2               P-0010           15            1500            3              0       ', 
					'    2               P-0011           48            1000            1              0       ', 
					'    2               P-0012           8              1              1              0       ', 
					'    2               P-0013          007            700             1              0       ', 
					'  1                 P-0014           13            1000            2              0       ', 
					'    2               P-0015          144            2000            1              0       ', 
					'    2               P-0016           15            1500            1              0       ', 
					'    2               P-0017           48            1000            1              0       ', 
					'    2               P-0018           8              1              1              0       ', 
					'    2               P-0019          007            700             1              0       ', 
					'      3             P-0020          135            1000            1              0       ', 
					'      3             P-0021          400             10             1              0       ', 
					'      3             P-0022          600            2000            1             2000     ', 
					'    2               P-0023          007            800             1             800      ', 
					'  1                 P-0024           12             1              5              5       ', 
					'  1                 P-0025           12             1              5              5       ', 
					'  1                 P-0026          145             90             1              0       ', 
					'  1                 P-0027          165            900             1              0       ', 
					''])

	def __expected_xml_output(self):
		return '\n'.join(['<?xml version="1.0" encoding="ISO-8859-1"?>', '<parts>', 
			'  <part><level>1</level><part_number>P-0001</part_number><source_code>1</source_code><unit_cost>1000</unit_cost><quantity>2</quantity><cost>2000</cost></part>', 
			'  <part><level>1</level><part_number>P-0002</part_number><source_code>1</source_code><unit_cost>1000</unit_cost><quantity>2</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0003</part_number><source_code>120</source_code><unit_cost>2000</unit_cost><quantity>2</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0004</part_number><source_code>11</source_code><unit_cost>1500</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0005</part_number><source_code>78</source_code><unit_cost>100</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0006</part_number><source_code>007</source_code><unit_cost>700</unit_cost><quantity>2</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0007</part_number><source_code>007</source_code><unit_cost>700</unit_cost><quantity>2</quantity><cost>1400</cost></part>', 
			'  <part><level>1</level><part_number>P-0008</part_number><source_code>13</source_code><unit_cost>1000</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0009</part_number><source_code>12</source_code><unit_cost>2000</unit_cost><quantity>1</quantity><cost>2000</cost></part>', 
			'  <part><level>2</level><part_number>P-0010</part_number><source_code>15</source_code><unit_cost>1500</unit_cost><quantity>3</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0011</part_number><source_code>48</source_code><unit_cost>1000</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0012</part_number><source_code>8</source_code><unit_cost>1</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0013</part_number><source_code>007</source_code><unit_cost>700</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>1</level><part_number>P-0014</part_number><source_code>13</source_code><unit_cost>1000</unit_cost><quantity>2</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0015</part_number><source_code>144</source_code><unit_cost>2000</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0016</part_number><source_code>15</source_code><unit_cost>1500</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0017</part_number><source_code>48</source_code><unit_cost>1000</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0018</part_number><source_code>8</source_code><unit_cost>1</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>2</level><part_number>P-0019</part_number><source_code>007</source_code><unit_cost>700</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>3</level><part_number>P-0020</part_number><source_code>135</source_code><unit_cost>1000</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>3</level><part_number>P-0021</part_number><source_code>400</source_code><unit_cost>10</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>3</level><part_number>P-0022</part_number><source_code>600</source_code><unit_cost>2000</unit_cost><quantity>1</quantity><cost>2000</cost></part>', 
			'  <part><level>2</level><part_number>P-0023</part_number><source_code>007</source_code><unit_cost>800</unit_cost><quantity>1</quantity><cost>800</cost></part>', 
			'  <part><level>1</level><part_number>P-0024</part_number><source_code>12</source_code><unit_cost>1</unit_cost><quantity>5</quantity><cost>5</cost></part>', 
			'  <part><level>1</level><part_number>P-0025</part_number><source_code>12</source_code><unit_cost>1</unit_cost><quantity>5</quantity><cost>5</cost></part>', 
			'  <part><level>1</level><part_number>P-0026</part_number><source_code>145</source_code><unit_cost>90</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'  <part><level>1</level><part_number>P-0027</part_number><source_code>165</source_code><unit_cost>900</unit_cost><quantity>1</quantity><cost>0</cost></part>', 
			'</parts>'])
