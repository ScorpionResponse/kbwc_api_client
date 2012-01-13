'''
An implementation of an OpenURL API client for the KB.
'''

from ApiClient import HttpApiClient
import logging
import urllib2

RFR_ID = "info/sid:oclc.org/KBWCpy"

class OpenURL(HttpApiClient):
    '''Basic OpenURL API that can resolve article citations to links.'''

    fields = ['title', 'issn', 'eissn', 'isbn', 'oclcnum', 'date',
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
                if i in fields:
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
                q += "%s=%s&" % (i, escaped_val)
        q += "rft.institution_id=%s&" % (self.institution_id,)
        q += "rfr_id=%s&" % (RFR_ID,)
        if self.wskey:
            q += "wskey=%s&" % (self.wskey,)
        if self.response_format == "json":
            q += "svc_id=json&"
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
            d = feedparser.parse(response)
            if d.bozo:
                # 'bozo' is set by feedparser if the XML does not parse correctly
                self.LOG.warn("%s - %s\n" % (d.bozo_exception.getLineNumber(), d.bozo_exception.getMessage()))
            return self._xml_reformat(d)
        return None
    
    def _json_reformat(self, jsondata):
        return jsondata

    def _xml_reformat(self, xmldata):
        return xmldata
