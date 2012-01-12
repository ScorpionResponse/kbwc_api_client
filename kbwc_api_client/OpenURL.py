'''
An implementation of an OpenURL API client for the KB.
'''

from ApiClient import HttpApiClient
import logging


class OpenURL(HttpApiClient):
    '''Basic OpenURL API that can resolve article citations to links.'''

    fields = ['title', 'issn', 'oclcnum', 'isbn', 'content', 'atitle'
              'aulast', 'volume', 'issue', 'spage']

    def __init__(self, institution_id, wskey, url_base="http://worldcat.org/webservices/kb/", response_format="xml"):
        HttpApiClient.__init__(self, institution_id, wskey, url_base, response_format)

    def openurl_query(self, **kwargs):
        '''OpenURL query uses:
             * title
             * issn
             * oclcnum
             * isbn
             * content (ebook, print, fulltext)
             * atitle
             * aulast
             * volume
             * issue
             * spage
        '''
        query_url = self.url_base + 'openurl/resolve' + self.create_query_string(map(self._to_openurl_1_0, kwargs))
        return self.execute_query(query_url)

    def _to_openurl_1_0(self, field):
        if field in fields:
            return 'rft.' + field
