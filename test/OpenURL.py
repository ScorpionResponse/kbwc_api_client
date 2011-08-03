import unittest
from client.OpenURL import OpenURL
import sys


class OpenURLTest(unittest.TestCase):
    """
    Test OpenURL queries
    """

    def setUp(self):
        pass


def suite():
    suite = unittest.makeSuite(OpenURLTest, 'test')
    return suite

if __name__ == "__main__":
    unittest.main()
