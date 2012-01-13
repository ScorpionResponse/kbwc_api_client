"""
The ApiClient module defines base classes for the different
KBWC APIs.  Only HTTP APIs are currently supported.
"""

import logging
import urllib2
from version import __version__

USER_AGENT = "KBWCpy (%s)" % (__version__,)


class HttpApiClient:
    """
    HttpApiClient is a helper class to provide a base of functionality
    for all clients of the different types of API queries that use HTTP.

    This class should never be called directly.  Instead use
    either the OpenURL or Rest classes for that type of API.
    """

    LOG = logging.getLogger("ApiClient")

    def __init__(self, institution_id, wskey, url_base="http://worldcat.org/webservices/kb/", response_format="xml"):
        self.institution_id = institution_id
        self.wskey = wskey
        self.url_base = url_base
        self.response_format = response_format

    def create_query_string(self, **kwargs):
        '''Format the arguments into a query string.

           Certain arguments are rewritten slightly to use the API conventions.
           institution_id and wskey are always added.
        '''
        q = '?'
        # Mostly this is here because "start-index" is unpythonic
        mapping = {'keyword': 'q',
                   'start_index': 'start-index',
                   'max_results': 'max-results',
                   'order_by': 'order-by'}
        for i in kwargs:
            if kwargs[i] is not None:
                try:
                    escaped_val = urllib2.quote(kwargs[i])
                except:
                    # This will happen when the value is not a string
                    escaped_val = kwargs[i]

                if i in mapping:
                    q += "%s=%s&" % (mapping[i], escaped_val)
                else:
                    q += "%s=%s&" % (i, escaped_val)
        q += "institution_id=%s&" % (self.institution_id,)
        if self.wskey:
            q += "wskey=%s&" % (self.wskey,)
        if self.response_format == "json":
            q += "alt=json&"
        return q.rstrip('&')

    def get_response(self, query):
        '''Retrieves a response from the server and does minimal handling of response codes.

           Most clients should use execute_query(query) instead of this unless access
           to the raw response is required.
           Returns None if there was a problem.
        '''
        self.LOG.info("Calling URL: %s" % (query,))
        headers = {'User-Agent': USER_AGENT}
        if self.response_format == 'json':
            headers['Accept'] = 'application/json'
        elif self.response_format == 'xml':
            headers['Accept'] = 'application/atom+xml'
        request = urllib2.Request(query, headers=headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            self.LOG.warn("Status code %s from URL '%s'\n" % (e.code, query))
            return None
        except urllib2.URLError, e:
            self.LOG.warn("Problem making the requests for URL '%s'. Exception: %s\n" % (query, e))
            return None
        self.LOG.debug("Status code %s from URL '%s'\n" % (response.code, query))
        return response

    def execute_query(self, query):
        '''All subclasses should override this to provide some additional response handling.'''
        raise NotImplementedError("This should be implemented in a subclass.")
