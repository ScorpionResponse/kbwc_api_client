from kbwc_api_client.OpenURL import OpenURL
import unittest

class OpenURLTest(unittest.TestCase):
    '''
    Test the OpenURL query client
    '''

    def setUp(self):
        inst_id = 111637
        wskey = 'TjBKm4f7QdZwxUrvfnukshyAIPkCgt3ZieslDR23Z95rV8rmqU3gIFvKRRDaTwX4UwzoQtQYIbyCqEWe'
        self.client_json = OpenURL(inst_id, wskey, response_format="json")
        self.client_xml = OpenURL(inst_id, wskey, response_format="xml")

    def tearDown(self):
        pass

    def testMapping(self):
        '''create_query_params should do some mappings between incoming parameters and the 
           actual values that will be used to do a kbwc query'''
        self.assertIn('rft.title', self.client_json.create_query_params(title='test title'))
        self.assertNotIn('rft.foo', self.client_json.create_query_params(foo='test value'))
        self.assertIn('rft.id', self.client_json.create_query_params(doi='abc123'))
        self.assertIn('rft.id', self.client_json.create_query_params(pmid='abc123'))

    def testAdditionalFields(self):
        '''create_query_params should always add some additional fields'''
        self.assertIn('rft.institution_id', self.client_json.create_query_params(keyword='test'))
        self.assertIn('wskey', self.client_json.create_query_params(keyword='test'))
        self.assertIn('rfr_id', self.client_json.create_query_params(keyword='test'))
    
    def testAltFormat(self):
        self.assertIn('svc_id', self.client_xml.create_query_params(keyword='test'))
        self.assertIn('svc_id', self.client_json.create_query_params(keyword='test'))
        self.assertEqual('xml', self.client_xml.create_query_params(keyword='test')['svc_id'])
        self.assertEqual('json', self.client_json.create_query_params(keyword='test')['svc_id'])
        self.assertNotEqual('json', self.client_xml.create_query_params(keyword='test')['svc_id'])
        self.assertNotEqual('xml', self.client_json.create_query_params(keyword='test')['svc_id'])

def suite():
    suite = unittest.makeSuite(OpenURLTest, 'test')
    return suite

if __name__ == "__main__":
    unittest.main()
