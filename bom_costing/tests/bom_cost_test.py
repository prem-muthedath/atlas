#!/usr/bin/python

from domain.configuration import BomBuilder
from domain.model.costs import AssemblyCost
from views.text import BomTextView


def configure():
	# Set up -- configuration
	# addItem(level, code, cost, quantity)
	builder=BomBuilder()
	builder.add_item(1,'1',1000,2)  # 1000*2  
	builder.add_item(1,'1',1000,2)  # Duplicate - NOT costed!!!

	builder.add_item(2,'120',2000,2)
	builder.add_item(2,'11',1500,1)
	builder.add_item(2,'78',100,1)
	builder.add_item(2,'007',700,2) # Duplicate to the leaf below - NOT Costed!!
	builder.add_item(2,'007',700,2)  # 700*2

	builder.add_item(1,'13',1000,1) 

	builder.add_item(2,'12',2000,1)  # 2000*1
	builder.add_item(2,'15',1500,3)
	builder.add_item(2,'48',1000,1)
	builder.add_item(2,'8',1,1)
	builder.add_item(2,'007',700,1)

	builder.add_item(1,'13',1000,2)

	builder.add_item(2,'144',2000,1)  
	builder.add_item(2,'15',1500,1)
	builder.add_item(2,'48',1000,1)
	builder.add_item(2,'8',1,1)
	builder.add_item(2,'007',700,1)  # not costed, because it is NOT a leaf at level 2!!

	builder.add_item(3,'135',1000,1)
	builder.add_item(3,'400',10,1)
	builder.add_item(3,'600',2000,1)  # 2000*1 

	builder.add_item(2,'007',800,1)  # 800*1  This is a leaf at level 2

	builder.add_item(1,'12',1,5)  # 1*5
	builder.add_item(1,'12',1,5)  # 1*5
	builder.add_item(1,'145',90,1) #145 -- Not costed!!!
	builder.add_item(1,'165',900,1)

	return builder.build()


bom=configure()
bomcost=AssemblyCost()
bom.cost(bomcost)

bom_view=BomTextView()
bom.export(bom_view)

print bom_view.render()
print "EXPECTED: 8210 ", "ACTUAL: ", bomcost

