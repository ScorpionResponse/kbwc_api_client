import unittest
from client.Rest import Rest
import sys
class RestTest(unittest.TestCase):
    """
    Test Rest queries
    """

    def setUp(self):
        inst_id = 6569
        wskey = '4QpcmGhh34L7LLeo7p5PNJAsz14fQtyihkeGSgEUVFB33EWkocQ3JnNQ5A6wvzKAYxRYokTzeIFdOvG4'
        url_base = 'http://kbwcap02dxdu.dev.oclc.org:8080/kbwc-grid/'
        self.client_json = Rest(inst_id, wskey, url_base, "json")
        self.client_xml = Rest(inst_id, wskey, url_base)

    def testGetProvider(self):
        npg_xml = self.client_xml.get_provider('NPG')
        npg_json = self.client_json.get_provider('NPG')
        self.assertEqual(len(npg_xml), 1)
        self.assertEqual(len(npg_json), 1)
        self.assertEqual(npg_xml[0]['id'], npg_json[0]['id'])

def suite():
    suite = unittest.makeSuite(RestTest, 'test')
    return suite

if __name__ == "__main__":
    unittest.main()

