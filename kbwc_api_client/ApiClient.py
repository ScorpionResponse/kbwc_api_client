"""
The ApiClient module defines base classes for the different
KBWC APIs.  Only HTTP APIs are currently supported.
"""

import logging
import requests
from .version import __version__

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

    def create_query_params(self, **kwargs):
        '''All subclasses should override this to provide some additional response handling.'''
        raise NotImplementedError("This should be implemented in a subclass.")

#        '''Format the arguments into a query string.
#
#           Certain arguments are rewritten slightly to use the API conventions.
#           institution_id and wskey are always added.
#        '''
#        payload = {}
#        for i in kwargs:
#            if kwargs[i] is not None:
#                payload[i] = kwargs[i]
#        payload['institution_id'] = self.institution_id
#        if self.wskey:
#            q += "wskey=%s&" % (self.wskey,)
#            payload['wskey'] = self.wskey
#        payload['alt'] = self.response_format
#        return payload

    def get_response(self, query_url, params):
        '''Retrieves a response from the server and does minimal handling of response codes.

           Most clients should use execute_query(query) instead of this unless access
           to the raw response is required.
           Returns None if there was a problem.
        '''
        self.LOG.info("Calling URL: '%s' with params %s" % (query_url, params))
        headers = {'User-Agent': USER_AGENT}
        if self.response_format == 'json':
            headers['Accept'] = 'application/json'
        elif self.response_format == 'xml':
            headers['Accept'] = 'application/atom+xml'
        try:
            r = requests.get(query_url, params=params, headers=headers)
            #self.LOG.debug("Response data from server: %s" % (response.read(),))
        except ConnectionError, e:
            self.LOG.warn("Problem making the requests for URL '%s'. Exception: %s\n" % (query_url, e))
            return None

        if r.status_code == requests.codes.ok:
            self.LOG.debug("Status code %s from URL '%s'\n" % (r.status_code, query_url))
        else:
            self.LOG.warn("Status code %s from URL '%s'\n" % (r.status_code, query_url))
            return None
        return r.text

    def execute_query(self, query):
        '''All subclasses should override this to provide some additional response handling.'''
        raise NotImplementedError("This should be implemented in a subclass.")
