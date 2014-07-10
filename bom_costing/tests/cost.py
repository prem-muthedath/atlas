#!/usr/bin/python

from . import base

from .. import domain

class Cost(base.Test):
	def test(self):
		cost=domain.model.costs.Cost()
		self.bom.cost(cost)		
		print('\n')
		self.assertEquals(str(cost), '8210')
		print "BOM TOTAL COST --> ", cost
		print('\n')

