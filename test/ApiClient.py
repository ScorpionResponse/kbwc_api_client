from kbwc_api_client.ApiClient import HttpApiClient
import sys
import unittest


class ApiClientTest(unittest.TestCase):
    """
    Test ApiClient
    """

    def setUp(self):
        inst_id = 6569
        wskey = '4QpcmGhh34L7LLeo7p5PNJAsz14fQtyihkeGSgEUVFB33EWkocQ3JnNQ5A6wvzKAYxRYokTzeIFdOvG4'
        url_base = 'http://kbwcap02dxdu.dev.oclc.org:8080/kbwc-grid/'
        self.client_json = HttpApiClient(inst_id, wskey, url_base, "json")
        self.client_xml = HttpApiClient(inst_id, wskey, url_base)

    def tearDown(self):
        pass

    def testExecuteNotImpl(self):
        '''The ApiClient class should not support execute_query() directly.'''
        with self.assertRaises(NotImplementedError):
            self.client_xml.execute_query('test_query')


def suite():
    suite = unittest.makeSuite(ApiClientTest, 'test')
    return suite

if __name__ == "__main__":
    unittest.main()
