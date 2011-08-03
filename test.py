import unittest
import test.Rest
import test.OpenURL
import sys

def suite():
    suite = unittest.TestSuite()
    suite.addTest(test.Rest.suite())
    suite.addTest(test.OpenURL.suite())
    return suite

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite())

