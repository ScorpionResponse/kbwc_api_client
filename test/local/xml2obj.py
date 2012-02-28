from kbwc_api_client.util.xml2obj import xml2obj
import sys
import unittest

class xml2objTest(unittest.TestCase):
    '''
    Test the xml2obj utility
    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTransform(self):
        xmldata = '''<rsp><record uid="28858" openaccess="yes" issn="1026-0226" provider_uid="DOAJ" institution_id="111637" collection_name="Directory of Open Access Journals (All titles)" url="http://www.hindawi.com/GetJournal.aspx?journal=ddns" publisher="Hindawi Publishing Corporation" oclcnum="49941253" content="fulltext" id="b2ac02d1083f2d7a2d1737ed9f18c436" title="Discrete Dynamics in Nature and Society" eissn="1607-887X" jsid="32953" coverage_enum="fulltext" coverage="fulltext@1996" oclcnums="477410262 475391867 49941253 614330191 488193094 423533018 55976874" jkey="ddns" collection_uid="DOAJ.Records" provider_name="Directory of Open Access Journals" /></rsp>'''
        object_goal = {u'record': {u'collection_name': u'Directory of Open Access Journals (All titles)',
                                   u'collection_uid': u'DOAJ.Records',
                                   u'content': u'fulltext',
                                   u'coverage': u'fulltext@1996',
                                   u'coverage_enum': u'fulltext',
                                   u'eissn': u'1607-887X',
                                   u'id': u'b2ac02d1083f2d7a2d1737ed9f18c436',
                                   u'institution_id': u'111637',
                                   u'issn': u'1026-0226',
                                   u'jkey': u'ddns',
                                   u'jsid': u'32953',
                                   u'oclcnum': u'49941253',
                                   u'oclcnums': u'477410262 475391867 49941253 614330191 488193094 423533018 55976874',
                                   u'openaccess': u'yes',
                                   u'provider_name': u'Directory of Open Access Journals',
                                   u'provider_uid': u'DOAJ',
                                   u'publisher': u'Hindawi Publishing Corporation',
                                   u'title': u'Discrete Dynamics in Nature and Society',
                                   u'uid': u'28858',
                                   u'url': u'http://www.hindawi.com/GetJournal.aspx?journal=ddns'}}
        result = xml2obj(xmldata).get_result()
        self.assertEquals(result, object_goal)

def suite():
    suite = unittest.makeSuite(xml2objTest, 'test')
    return suite

if __name__ == "__main__":
    unittest.main()
