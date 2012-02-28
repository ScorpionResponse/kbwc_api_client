'''
An implementation of an OpenURL API client for the KB.
'''

from ApiClient import HttpApiClient
import logging
try:
    import json
except ImportError:
    import simplejson as json
import urllib2
from util.xml2obj import xml2obj

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
        query_url = self.url_base + 'openurl/resolve' + self.create_query_string(**kwargs)
        return self.execute_query(query_url)

    def create_query_string(self, **kwargs):
        '''Format the arguments into a query string.

           Certain arguments are rewritten slightly to use the API conventions.
           institution_id and wskey are always added.
        '''
        q = '?'
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

                try:
                    escaped_val = urllib2.quote(kwargs[i])
                except:
                    # This will happen when the value is not a string
                    escaped_val = kwargs[i]
                q += "%s=%s&" % (field_name, escaped_val)
        q += "rft.institution_id=%s&" % (self.institution_id,)
        q += "rfr_id=%s&" % (RFR_ID,)
        if self.wskey:
            q += "wskey=%s&" % (self.wskey,)
        if self.response_format == "json":
            q += "svc_id=json&"
        elif self.response_format == "xml":
            q += "svc_id=xml&"
        return q.rstrip('&')

    def execute_query(self, query):
        '''Calls the api with a particular query string and does some basic response parsing.'''
        response = self.get_response(query)
        if response is None:
            return None
        if self.response_format == "json":
            d = json.load(response, encoding="UTF-8")
            return self._json_reformat(d)
        else:
            d = xml2obj(response)
            return self._xml_reformat(d.get_result())
        return None
    
    def _json_reformat(self, jsondata):
        self.LOG.debug("JSON Data from server: %s" % (jsondata,))
        return jsondata

    def _xml_reformat(self, xmldata):
        self.LOG.debug("XML Data from server: %s" % (xmldata,))
        return xmldata['record']
