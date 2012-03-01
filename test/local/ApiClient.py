from kbwc_api_client.ApiClient import HttpApiClient
import sys
import unittest


class ApiClientTest(unittest.TestCase):
    """
    Test ApiClient
    """

    def setUp(self):
        inst_id = 111637
        wskey = 'TjBKm4f7QdZwxUrvfnukshyAIPkCgt3ZieslDR23Z95rV8rmqU3gIFvKRRDaTwX4UwzoQtQYIbyCqEWe'
        self.client_json = HttpApiClient(inst_id, wskey, response_format="json")
        self.client_xml = HttpApiClient(inst_id, wskey)

    def tearDown(self):
        pass

    def testExecuteNotImpl(self):
        '''The ApiClient class should not support execute_query() directly.'''
        with self.assertRaises(NotImplementedError):
            self.client_xml.execute_query('test_query')

    def testExecuteNotImpl(self):
        '''The ApiClient class should not support create_query_paramsy() directly.'''
        with self.assertRaises(NotImplementedError):
            self.client_xml.create_query_params(keyword='test_query')


def suite():
    suite = unittest.makeSuite(ApiClientTest, 'test')
    return suite

if __name__ == "__main__":
    unittest.main()
