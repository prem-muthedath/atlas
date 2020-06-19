import unittest

from ..atlas import Atlas
from ..schema import _Schema
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
        report=self._app.text_report()
        self.assertEqual(report, reports.default_text())
        print "default TEXT report =>", "\n", reports.default_text()

class TestCustomTextReport(Test):
    def _assert(self):
        schema=[_Schema.level, _Schema.part_number, _Schema.cost]
        report=self._app.text_report(schema)
        self.assertEqual(report, reports.custom_text())
        print "custom TEXT report =>", "\n", reports.custom_text()

################################################################################

class TestDefaultXmlReport(Test):
    def _assert(self):
        report=self._app.xml_report()
        self.assertEqual(report, reports.default_xml())
        print "default XML report =>", "\n", reports.default_xml()

class TestCustomXmlReport(Test):
    def _assert(self):
        schema=[_Schema.level, _Schema.part_number, _Schema.cost]
        report=self._app.xml_report(schema)
        self.assertEqual(report, reports.custom_xml())
        print "custom XML report =>", "\n", reports.custom_xml()

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
