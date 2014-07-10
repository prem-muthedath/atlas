#!/usr/bin/python

from . import test

from .. import domain

class Cost(test.Test):
	def test(self):
		cost=domain.model.costs.Cost()
		self.bom.cost(cost)		
		print('\n')
		self.assertEquals(str(cost), '8210')
		print "BOM TOTAL COST --> ", cost
		print('\n')

