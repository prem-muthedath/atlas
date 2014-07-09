#!/usr/bin/python

from .. import domain
from .. import export

def configure():
	# Set up -- configuration
	# addItem(level, number, code, cost, quantity)
	builder=domain.configuration.BomBuilder()
	builder.add_item(1,'P-0001','1',1000,2)  # 1000*2  
	builder.add_item(1,'P-0002','1',1000,2)  # Duplicate - NOT costed!!!

	builder.add_item(2,'P-0003','120',2000,2)
	builder.add_item(2,'P-0004','11',1500,1)
	builder.add_item(2,'P-0005','78',100,1)
	builder.add_item(2,'P-0006','007',700,2) # Duplicate to the leaf below - NOT Costed!!
	builder.add_item(2,'P-0007','007',700,2)  # 700*2

	builder.add_item(1,'P-0008','13',1000,1) 

	builder.add_item(2,'P-0009','12',2000,1)  # 2000*1
	builder.add_item(2,'P-0010','15',1500,3)
	builder.add_item(2,'P-0011','48',1000,1)
	builder.add_item(2,'P-0012','8',1,1)
	builder.add_item(2,'P-0013','007',700,1)

	builder.add_item(1,'P-0014','13',1000,2)

	builder.add_item(2,'P-0015','144',2000,1)  
	builder.add_item(2,'P-0016','15',1500,1)
	builder.add_item(2,'P-0017','48',1000,1)
	builder.add_item(2,'P-0018','8',1,1)
	builder.add_item(2,'P-0019','007',700,1)  # not costed, because it is NOT a leaf at level 2!!

	builder.add_item(3,'P-0020','135',1000,1)
	builder.add_item(3,'P-0021','400',10,1)
	builder.add_item(3,'P-0022','600',2000,1)  # 2000*1 

	builder.add_item(2,'P-0023','007',800,1)  # 800*1  This is a leaf at level 2

	builder.add_item(1,'P-0024','12',1,5)  # 1*5
	builder.add_item(1,'P-0025','12',1,5)  # 1*5
	builder.add_item(1,'P-0026','145',90,1) #145 -- Not costed!!!
	builder.add_item(1,'P-0027','165',900,1)

	return builder.build()

def run():
	bom=configure()
	cost=domain.model.costs.Cost()
	bom.cost(cost)
	print('\n')
	print "BOM TOTAL COST --> EXPECTED: 8210 ", "ACTUAL: ", cost

	#########################################################################################
	#### DEFAULT DISPLAYS -- INCLUDES ALL PART ATTRIBUTES, IN THE ORDER DEFINED IN PartSchema
	#########################################################################################
	print('\n\n'+'DEFAULT TEXT OUTPUT -- INCLUDES ALL PART ATTRIBUTES IN THE DEFAULT ORDER:\n')
	print export.exports.text_export(bom)
	print('\n\n'+'DEFAULT XML OUTPUT -- INCLUDES ALL PART ATTRIBUTES IN THE DEFAULT ORDER:\n')
	print export.exports.xml_export(bom)

	#########################################################################################
	#### CUSTOMISED DISPLAYS -- PART ATTRIBUTES AND THEIR ORDER CHOSEN BY USER
	#########################################################################################
	part_attributes=[export.base.PartSchema.NUMBER, export.base.PartSchema.LEVEL, export.base.PartSchema.COST]
	print('\n\n'+'CUSTOMISED TEXT OUTPUT -- USER-SELECTED PART ATTRIBUTES AND PART-ATTRIBUTE ORDERING:\n')
	print export.exports.text_export(bom, part_attributes)
	print('\n\n'+'CUSTOMISED XML OUTPUT -- USER-SELECTED PART ATTRIBUTES AND PART-ATTRIBUTE ORDERING:\n')
	print export.exports.xml_export(bom, part_attributes)
