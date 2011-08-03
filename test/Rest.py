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

    def testListProviders(self):
        xml = self.client_xml.list_providers()
        json = self.client_json.list_providers()
        self.assertEqual(len(xml), len(json))

    def testSearchProviders(self):
        xml = self.client_xml.search_providers('Nature')
        json = self.client_json.search_providers('Nature')
        self.assertEqual(len(xml), len(json))

    def testGetProvider(self):
        npg_xml = self.client_xml.get_collection('NPG.journals')
        npg_json = self.client_json.get_collection('NPG.journals')
        self.assertEqual(len(npg_xml), 1)
        self.assertEqual(len(npg_json), 1)
        self.assertEqual(npg_xml[0]['id'], npg_json[0]['id'])

    def testGetEntrybyID(self):
        entry_xml = self.client_xml.get_entry('036f688a982b7a702aadd05003f9742e')
        entry_json = self.client_json.get_entry('036f688a982b7a702aadd05003f9742e')
        self.assertEqual(len(entry_xml), 1)
        self.assertEqual(len(entry_json), 1)
        self.assertEqual(entry_xml[0]['id'], entry_json[0]['id'])

    def testGetEntrybyUID(self):
        entry_xml = self.client_xml.get_entry('NPG.journals,1987357')
        entry_json = self.client_json.get_entry('NPG.journals,1987357')
        self.assertEqual(len(entry_xml), 1)
        self.assertEqual(len(entry_json), 1)
        self.assertEqual(entry_xml[0]['id'], entry_json[0]['id'])

def suite():
    suite = unittest.makeSuite(RestTest, 'test')
    return suite

if __name__ == "__main__":
    unittest.main()
