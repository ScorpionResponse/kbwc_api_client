'''
An implementation of an OpenURL API client for the KB.
'''

from ApiClient import HttpApiClient
import logging


class OpenURL(HttpApiClient):
    '''Basic OpenURL API that can resolve article citations to links.'''

    def __init__(self, institution_id, wskey, url_base, response_format="xml"):
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
        pass
