from kbwc_api_client.OpenURL import OpenURL
import unittest


class OpenURLTest(unittest.TestCase):
    """
    Test OpenURL queries
    """

    def setUp(self):
        inst_id = 111637
        wskey = 'TjBKm4f7QdZwxUrvfnukshyAIPkCgt3ZieslDR23Z95rV8rmqU3gIFvKRRDaTwX4UwzoQtQYIbyCqEWe'
        self.client_json = OpenURL(inst_id, wskey, response_format="json")
        self.client_xml = OpenURL(inst_id, wskey, response_format="xml")

    def testOpenURL(self):
        '''Compare the result size of the XML and JSON openurl calls'''
        xml = self.client_xml.openurl_query(title='Discrete Dynamics in Nature and Society', issn='1026-0226')
        json = self.client_json.openurl_query(title='Discrete Dynamics in Nature and Society', issn='1026-0226')
        self.assertEqual(len(xml), len(json))

    def testResponseEqual(self):
        '''Compare the exact contents of the XML and JSON results'''
        xml = self.client_xml.openurl_query(title='Discrete Dynamics in Nature and Society', issn='1026-0226')
        json = self.client_json.openurl_query(title='Discrete Dynamics in Nature and Society', issn='1026-0226')
        self.assertEqual(xml, json)

    def tearDown(self):
        pass

def suite():
    suite = unittest.makeSuite(OpenURLTest, 'test')
    return suite

if __name__ == "__main__":
    unittest.main()
