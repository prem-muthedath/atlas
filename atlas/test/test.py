import unittest

from ..configuration import _BomBuilder
from ..schema import _Schema
from ..report import (TextReport, XmlReport,)
from . import report

# test module -- contains all unit tests for atlas application.
################################################################################

class Test(unittest.TestCase):
    def setUp(self):
        # Set up -- configuration
        # addItem(level, number, code, cost, quantity)
        builder=_BomBuilder()
        builder.add_item(1, 'P-0001', '1', 1000, 2)  # 1000*2
        builder.add_item(1, 'P-0002', '1', 1000, 2)  # Duplicate - NOT costed!!!

        builder.add_item(2, 'P-0003', '120', 2000, 2)
        builder.add_item(2, 'P-0004', '11', 1500, 1)
        builder.add_item(2, 'P-0005', '78', 100, 1)
        builder.add_item(2, 'P-0006', '007', 700, 2) # Duplicate to the leaf below - NOT Costed!!
        builder.add_item(2, 'P-0007', '007', 700, 2)  # 700*2

        builder.add_item(1, 'P-0008', '13', 1000, 1)

        builder.add_item(2, 'P-0009', '12', 2000, 1)  # 2000*1
        builder.add_item(2, 'P-0010', '15', 1500, 3)
        builder.add_item(2, 'P-0011', '48', 1000, 1)
        builder.add_item(2, 'P-0012', '8', 1, 1)
        builder.add_item(2, 'P-0013', '007', 700, 1)

        builder.add_item(1, 'P-0014', '13', 1000, 2)

        builder.add_item(2, 'P-0015', '144', 2000, 1)
        builder.add_item(2, 'P-0016', '15', 1500, 1)
        builder.add_item(2, 'P-0017', '48', 1000, 1)
        builder.add_item(2, 'P-0018', '8', 1, 1)
        builder.add_item(2, 'P-0019', '007', 700, 1)  # not costed, because it is NOT a leaf at level 2!!

        builder.add_item(3, 'P-0020', '135', 1000, 1)
        builder.add_item(3, 'P-0021', '400', 10, 1)
        builder.add_item(3, 'P-0022', '600', 2000, 1)  # 2000*1

        builder.add_item(2, 'P-0023', '007', 800, 1)  # 800*1  This is a leaf at level 2

        builder.add_item(1, 'P-0024', '12', 1, 5)  # 1*5
        builder.add_item(1, 'P-0025', '12', 1, 5)  # 1*5
        builder.add_item(1, 'P-0026', '145', 90, 1) #145 -- Not costed!!!
        builder.add_item(1, 'P-0027', '165', 900, 1)

        self.bom=builder.build()

    def tearDown(self):
        self.bom=None

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
        cost=self.bom.cost()
        self.assertEqual(cost, 8210)
        print "total bom cost =>", cost

class TestRerunTotalCost(Test):
    def _assert(self):
        cost1=self.bom.cost()
        cost2=self.bom.cost()
        self.assertEqual(cost1, 8210)
        self.assertEqual(cost2, 8210)
        print "total bom cost after run 1 & run 2, resp =>", cost1, "|", cost2

################################################################################

class TestDefaultTextReport(Test):
    def _assert(self):
        _report=TextReport()
        self.assertEqual(_report.render(self.bom), report.default_text())
        print "default TEXT report =>", "\n", report.default_text()

class TestCustomTextReport(Test):
    def _assert(self):
        schema=[_Schema.level, _Schema.part_number, _Schema.cost]
        _report=TextReport()
        self.assertEqual(_report.render(self.bom, schema), report.custom_text())
        print "custom TEXT report =>", "\n", report.custom_text()

################################################################################

class TestDefaultXmlReport(Test):
    def _assert(self):
        _report=XmlReport()
        self.assertEqual(_report.render(self.bom), report.default_xml())
        print "default XML report =>", "\n", report.default_xml()

class TestCustomXmlReport(Test):
    def _assert(self):
        schema=[_Schema.level, _Schema.part_number, _Schema.cost]
        _report=XmlReport()
        self.assertEqual(_report.render(self.bom, schema), report.custom_xml())
        print "custom XML report =>", "\n", report.custom_xml()

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
