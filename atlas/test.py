import unittest

from .configuration import _BomBuilder
from .schema import _Schema
from .report import (TextReport, XmlReport,)
from . import repo

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
        print "total cost =>", cost

class TestRerunTotalCost(Test):
    def _assert(self):
        cost1=self.bom.cost()
        cost2=self.bom.cost()
        self.assertEqual(cost1, 8210)
        self.assertEqual(cost2, 8210)
        print "total cost after re-run =>", cost1, "|", cost2

################################################################################

class TestDefaultTextReport(Test):
    def _assert(self):
        report=TextReport()
        self.assertEqual(report.render(self.bom), repo.default_text_report())
        print "default TEXT report =>", "\n", repo.default_text_report()

class TestCustomTextReport(Test):
    def _assert(self):
        report=TextReport([_Schema.level, _Schema.part_number, _Schema.cost])
        self.assertEqual(report.render(self.bom), repo.custom_text_report())
        print "custom TEXT report =>", "\n", repo.custom_text_report()

################################################################################

class TestDefaultXmlReport(Test):
    def _assert(self):
        report=XmlReport()
        self.assertEqual(report.render(self.bom), repo.default_xml_report())
        print "default XML report =>", "\n", repo.default_xml_report()

class TestCustomXmlReport(Test):
    def _assert(self):
        report=XmlReport([_Schema.level, _Schema.part_number, _Schema.cost])
        self.assertEqual(report.render(self.bom), repo.custom_xml_report())
        print "custom XML report =>", "\n", repo.custom_xml_report()

################################################################################

del(Test)

################################################################################

def main():
    # calls unittest.main() to run tests.
    # to use:
    #   1. call this method in atlas.__main__.py
    #   2. then run `python -m atlas` to execute runTest()
    #   3. ref: https://docs.python.org/2/library/unittest.html#unittest.main
    unittest.main(module='atlas.test')

################################################################################
