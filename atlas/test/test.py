import unittest

from ..atlas import Atlas
from ..schema import _Schema
from ..components import _Bom, _Part, _CostUnits
from . import report

# test module -- contains all unit tests for atlas application.
################################################################################

class Test(unittest.TestCase):
    def setUp(self):
        # Set up -- configuration
        self._app=Atlas()

    def tearDown(self):
        self._app=None

    def runTest(self):
        self._header()
        self._assert()

    def _header(self):
        # print test header
        print " ".join([
                        "\n",
                        "--------------------",
                        "TEST NAME:",
                        self.__class__.__name__,
                        "--------------------"
                    ])

    def _assert(self):
        # assert expected result
        pass

################################################################################

class TestTotalCost(Test):
    def _assert(self):
        cost=self._app.cost()
        self.assertEqual(cost, 8210)
        print "total bom cost =>", cost

class TestRerunTotalCost(Test):
    def _assert(self):
        cost1=self._app.cost()
        cost2=self._app.cost()
        self.assertEqual(cost1, 8210)
        self.assertEqual(cost2, 8210)
        print "total bom cost after run 1 & run 2, resp =>", cost1, "|", cost2

################################################################################

class TestDefaultTextReport(Test):
    def _assert(self):
        _report=self._app.text_report()
        self.assertEqual(_report, report.default_text())
        print "default TEXT report =>", "\n", report.default_text()

class TestCustomTextReport(Test):
    def _assert(self):
        schema=[_Schema.level, _Schema.part_number, _Schema.cost]
        _report=self._app.text_report(schema)
        self.assertEqual(_report, report.custom_text())
        print "custom TEXT report =>", "\n", report.custom_text()

################################################################################

class TestDefaultXmlReport(Test):
    def _assert(self):
        _report=self._app.xml_report()
        self.assertEqual(_report, report.default_xml())
        print "default XML report =>", "\n", report.default_xml()

class TestCustomXmlReport(Test):
    def _assert(self):
        schema=[_Schema.level, _Schema.part_number, _Schema.cost]
        _report=self._app.xml_report(schema)
        self.assertEqual(_report, report.custom_xml())
        print "custom XML report =>", "\n", report.custom_xml()

################################################################################

class TestDuplicatePart(Test):
    def _assert(self):
        bom=_Bom()
        bom._add(_Part(bom, 'P-0001', '1', _CostUnits(20, 4)))
        self.assertRaises(RuntimeError,
                bom._add, _Part(bom,'P-0001', '12', _CostUnits(200, 1)))
        self.assertEquals(bom._positions(), [0])
        print "bom positions =>", bom._positions()

class TestDuplicateBom(Test):
    def _assert(self):
        bom=_Bom()
        bom1=_Bom()
        bom2=_Bom()
        bom1._add(_Part(bom, 'P-0001', '1', _CostUnits(20, 4)))
        bom2._add(_Part(bom, 'P-0001', '1', _CostUnits(20, 4)))
        bom._add(bom1)
        bom._add(bom2)
        self.assertRaises(RuntimeError, bom._add, bom1)
        self.assertEquals(bom._positions(), [0, 1])
        print "bom positions =>", bom._positions()

################################################################################

class TestNonCostableLeafChange(Test):
    def _assert(self):
        bom=_Bom()
        bom._add(_Part(bom, 'P-0001', '100', _CostUnits(20, 4)))
        bom._add(_Part(bom, 'P-0002', '100', _CostUnits(400, 4)))
        self.assertEquals(bom._cost(), 1600)
        print "bom cost & positions BEFORE leaf change =>", \
                bom._cost(), "|", bom._positions()
        bom._add(_Part(bom, 'P-0003', '200', _CostUnits(20, 4)))
        self.assertEquals(bom._cost(), 80)
        self.assertEquals(bom._cost(), 80)
        print "bom cost & positions AFTER leaf change =>", \
                bom._cost(), "|", bom._positions()

class TestCostableLeafChange(Test):
    def _assert(self):
        bom=_Bom()
        bom._add(_Part(bom, 'P-0001', '100', _CostUnits(20, 4)))
        bom._add(_Part(bom, 'P-0002', '1', _CostUnits(400, 4)))
        self.assertEquals(bom._cost(), 1600)
        print "bom cost & positions BEFORE leaf change =>", \
                bom._cost(), "|", bom._positions()
        bom._add(_Part(bom, 'P-0003', '200', _CostUnits(20, 4)))
        self.assertEquals(bom._cost(), 1600)
        self.assertEquals(bom._cost(), 1600)
        print "bom cost & positions AFTER leaf change =>", \
                bom._cost(), "|", bom._positions()

################################################################################

# `Test` deleted; else, unittest will run it.
# `Test` is a base class, & doesn't test anything, so need not run it.
# for del(Test) trick, see /u/ Wojciech B @ https://tinyurl.com/yb58qtae
del(Test)

################################################################################

def main():
    # calls unittest.main() to run tests.
    # to use:
    #   1. call this method in atlas.__main__.py
    #   2. then run `python -m atlas` to execute runTest()
    #   3. ref: https://docs.python.org/2/library/unittest.html#unittest.main
    unittest.main(module='atlas.test.test')

################################################################################
