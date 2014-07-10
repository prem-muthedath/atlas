#!/usr/bin/python

import unittest

from . import cost
from . import default
from . import custom

_LOADER = unittest.TestLoader()
_RUNNER = unittest.TextTestRunner(verbosity=2)

def tests(test_case):
    return _LOADER.loadTestsFromTestCase(test_case)

def run_all():
	suite=unittest.TestSuite()
	suite.addTest(tests(cost.Cost))
	suite.addTest(tests(default.Default))
	suite.addTest(tests(custom.Custom))
	_RUNNER.run(suite)




