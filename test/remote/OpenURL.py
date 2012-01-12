from kbwc_api_client.OpenURL import OpenURL
import sys
import unittest


class OpenURLTest(unittest.TestCase):
    """
    Test OpenURL queries
    """

    def setUp(self):
        inst_id = 111637
        wskey = 'TjBKm4f7QdZwxUrvfnukshyAIPkCgt3ZieslDR23Z95rV8rmqU3gIFvKRRDaTwX4UwzoQtQYIbyCqEWe'
        self.client_json = Rest(inst_id, wskey, response_format="json")
        self.client_xml = Rest(inst_id, wskey)

    def tearDown(self):
        pass

def suite():
    suite = unittest.makeSuite(OpenURLTest, 'test')
    return suite

if __name__ == "__main__":
    unittest.main()
