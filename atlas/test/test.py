import unittest

from ..atlas import Atlas
from ..schema import _Schema
from ..components import _Bom
from ..report import _TextReport, _XmlReport
from . import reports

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
        print (" ".join([
                        "\n",
                        "--------------------",
                        "TEST NAME:",
                        self.__class__.__name__,
                        "--------------------"
                    ]))

    def _assert(self):
        # assert expected result
        pass

################################################################################

class TestInvalidSchema(Test):
    def _assert(self):
        with self.assertRaises(AssertionError) as cn:
            schema=[_Schema.level, 'prem', _Schema.cost, 'lisa']
            self._app.text_report(schema)
        print ("exception: ", cn.exception.__class__.__name__, \
                "| msg => ", cn.exception)
        self.assertEqual(cn.exception.__str__(), 'bad report schema.')

class TestNullSchema(Test):
    def _assert(self):
        with self.assertRaises(AssertionError) as cn:
            schema=None
            self._app.text_report(schema)
        print ("exception: ", cn.exception.__class__.__name__, \
                "| msg => ", cn.exception)
        self.assertEqual(cn.exception.__str__(), 'report schema not iterable.')

class TestNonIterableSchema(Test):
    def _assert(self):
        with self.assertRaises(AssertionError) as cn:
            schema=_Schema.cost
            self._app.text_report(schema)
        print ("exception: ", cn.exception.__class__.__name__, \
                "| msg => ", cn.exception)
        self.assertEqual(cn.exception.__str__(), 'report schema not iterable.')

################################################################################

class TestEmptyBomCost(Test):
    def _assert(self):
        cost=_Bom([])._cost()
        self.assertEqual(cost, 0)
        print ("total bom cost =>", cost)

class TestTotalCost(Test):
    def _assert(self):
        cost=self._app.cost()
        self.assertEqual(cost, 9110)
        print ("total bom cost =>", cost)

class TestRerunTotalCost(Test):
    def _assert(self):
        bom=self._app._bom()
        cost1=bom._cost()
        cost2=bom._cost()
        self.assertEqual(cost1, 9110)
        self.assertEqual(cost2, 9110)
        print ("total bom cost after run 1 & run 2, resp =>", cost1, "|", cost2)

################################################################################

class TestEmptyBomTextReport(Test):
    def _assert(self):
        report=_TextReport(_Schema, [])._render()
        self.assertEqual(report, '')
        print ("empty BOM TEXT report =>", report)

class TestEmptySchemaTextReport(Test):
    def _assert(self):
        report=self._app.text_report([])
        self.assertEqual(report, '')
        print ("empty SCHEMA TEXT report =>", report)

################################################################################

class TestDefaultTextReport(Test):
    def _assert(self):
        report=self._app.text_report()
        self.assertEqual(report, reports.default_text())
        print ("default TEXT report =>", "\n", report)

class TestCustomTextReport(Test):
    def _assert(self):
        schema=[_Schema.part_number, _Schema.cost]
        report=self._app.text_report(schema)
        self.assertEqual(report, reports.custom_text())
        print ("custom TEXT report =>", "\n", report)

class TestCustomOrderedTextReport(Test):
    def _assert(self):
        schema=[_Schema.part_number, _Schema.costed, _Schema.quantity]
        report=self._app.text_report(schema)
        self.assertEqual(report, reports.custom_ordered_text())
        print ("custom ordered TEXT report =>", "\n", report)

class TestCustomNoTotalsTextReport(Test):
    def _assert(self):
        schema=[_Schema.part_number]
        report=self._app.text_report(schema)
        self.assertEqual(report, reports.custom_no_totals_text())
        print ("custom NO-TOTALS TEXT report =>", "\n", report)

################################################################################

class TestEmptyBomXmlReport(Test):
    def _assert(self):
        report=_XmlReport(_Schema, [])._render()
        self.assertEqual(report, '<xml></xml>')
        print ("empty BOM XML report =>", '\n', report)

class TestEmptySchemaXmlReport(Test):
    def _assert(self):
        report=self._app.xml_report([])
        self.assertEqual(report, '<xml></xml>')
        print ("empty SCHEMA XML report =>", '\n', report)

################################################################################

class TestDefaultXmlReport(Test):
    def _assert(self):
        report=self._app.xml_report()
        self.assertEqual(report, reports.default_xml())
        print ("default XML report =>", "\n", report)

class TestCustomXmlReport(Test):
    def _assert(self):
        schema=[_Schema.level, _Schema.part_number, _Schema.cost]
        report=self._app.xml_report(schema)
        self.assertEqual(report, reports.custom_xml())
        print ("custom XML report =>", "\n", report)

class TestCustomOrderedXmlReport(Test):
    def _assert(self):
        schema=[_Schema.part_number, _Schema.costed, _Schema.quantity]
        report=self._app.xml_report(schema)
        self.assertEqual(report, reports.custom_ordered_xml())
        print ("custom ordered XML report =>", "\n", report)

class TestCustomNoTotalsXmlReport(Test):
    def _assert(self):
        schema=[_Schema.level, _Schema.part_number]
        report=self._app.xml_report(schema)
        self.assertEqual(report, reports.custom_no_totals_xml())
        print ("custom NO-TOTALS XML report =>", "\n", report)

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
