import unittest
import test.remote
import test.local
import sys
import logging


def suite(inc_remote=False):
    LOG = logging.getLogger()
    LOG.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    #ch.setLevel(logging.INFO)
    LOG.addHandler(ch)
    suite = unittest.TestSuite()
    suite.addTest(test.local.ApiClient.suite())
    if inc_remote:
        suite.addTest(test.remote.Rest.suite())
        suite.addTest(test.remote.OpenURL.suite())
    return suite


include_remote_tests = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'remote':
        print 'Including Remote tests.'
        include_remote_tests = True

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite(include_remote_tests))


    
