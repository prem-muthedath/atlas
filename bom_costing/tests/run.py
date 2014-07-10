#!/usr/bin/python

import unittest

from . import cost
from . import default
from . import custom

_LOADER = unittest.TestLoader()
_RUNNER = unittest.TextTestRunner(verbosity=2)

def load_test_case(test_case):
    return _LOADER.loadTestsFromTestCase(test_case)

def run_all():
	suite=unittest.TestSuite()
	suite.addTest(load_test_case(cost.Cost))
	suite.addTest(load_test_case(default.Default))
	suite.addTest(load_test_case(custom.Custom))
	_RUNNER.run(suite)




