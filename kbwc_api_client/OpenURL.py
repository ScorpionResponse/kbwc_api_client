'''
An implementation of an OpenURL API client for the KB.
'''

from .ApiClient import HttpApiClient
import logging
try:
    import json
except ImportError:
    import simplejson as json
from .util.xml2obj import xml2obj

RFR_ID = "info/sid:oclc.org/KBWCpy"

class OpenURL(HttpApiClient):
    '''Basic OpenURL API that can resolve article citations to links.'''

    openurl_fields = ['title', 'issn', 'eissn', 'isbn', 'oclcnum', 'date',
                      'volume', 'issue', 'spage', 'epage', 'atitle', 'aulast',
                      'provider_uid', 'collection_uid', 'content', 'jkey', 'openaccess']

    def __init__(self, institution_id, wskey, url_base="http://worldcat.org/webservices/kb/", response_format="xml"):
        HttpApiClient.__init__(self, institution_id, wskey, url_base, response_format)

    def openurl_query(self, **kwargs):
        '''OpenURL query uses:
             * title
             * issn
             * eissn
             * isbn
             * oclcnum
             * date
             * volume
             * issue
             * spage
             * epage
             * atitle
             * aulast
             * provider_uid
             * collection_uid
             * content (ebook, print, fulltext)
             * jkey
             * openaccess
             * pmid
             * doi
        '''
        query_url = self.url_base + 'openurl/resolve' 
        params = self.create_query_params(**kwargs)
        return self.execute_query(query_url, params)

    def create_query_params(self, **kwargs):
        '''Format the arguments into a query string.

           Certain arguments are rewritten slightly to use the API conventions.
           institution_id and wskey are always added.
        '''
        payload = {}
        for i in kwargs:
            if kwargs[i] is not None:
                field_name = i
                if i in self.openurl_fields:
                    field_name = 'rft.' + i
                elif i == 'pmid':
                    field_name = 'rft.id'
                    kwargs[i] = 'info:pmid/' + kwargs[i]
                elif i == 'doi':
                    field_name = 'rft.id'
                    kwargs[i] = 'info:doi/' + kwargs[i]

                payload[field_name] = kwargs[i]
        payload["rft.institution_id"] = self.institution_id
        payload["rfr_id"] = RFR_ID
        if self.wskey:
            payload["wskey"] = self.wskey
        payload["svc_id"] = self.response_format
        return payload

    def execute_query(self, query_url, params):
        '''Calls the api with a particular query string and does some basic response parsing.'''
        response = self.get_response(query_url, params)
        if response is None:
            return None
        if self.response_format == "json":
            return self._json_reformat(response)
        else:
            return self._xml_reformat(response)
        return None
    
    def _json_reformat(self, jsondata):
        self.LOG.debug("JSON Data from server: %s" % (jsondata,))
        ref = json.loads(jsondata, encoding="UTF-8")
        self.LOG.debug("JSON Data reformatted: %s" % (ref,))
        return ref

    def _xml_reformat(self, xmldata):
        self.LOG.debug("XML Data from server: %s" % (xmldata,))
        obj = xml2obj(xmldata.encode('utf-8'))
        d = obj.get_result()
        ref = d['record']
        for i in ref:
            i[u'institution_id'] = [i[u'institution_id']]
        self.LOG.debug("XML Data reformatted: %s" % (ref,))
        return ref
