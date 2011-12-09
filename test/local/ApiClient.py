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

    def testMapping(self):
        '''create_query_string should do some mappings to the right api field'''
        self.assertIn('q=', self.client_xml.create_query_string(keyword='test'))
        self.assertIn('start-index=', self.client_xml.create_query_string(start_index=10))
        self.assertIn('max-results=', self.client_xml.create_query_string(max_results=10))
        self.assertIn('order-by=', self.client_xml.create_query_string(order_by='title'))

    def testAdditionalFields(self):
        '''create_query_string should add some additional fields'''
        self.assertIn('institution_id=', self.client_xml.create_query_string(keyword='test'))
        self.assertIn('wskey=', self.client_xml.create_query_string(keyword='test'))

    def testAltFormat(self):
        self.assertIn('alt=json', self.client_json.create_query_string(keyword='test'))
        self.assertNotIn('alt=json', self.client_xml.create_query_string(keyword='test'))
        self.assertNotIn('alt=xml', self.client_json.create_query_string(keyword='test'))


def suite():
    suite = unittest.makeSuite(ApiClientTest, 'test')
    return suite

if __name__ == "__main__":
    unittest.main()
