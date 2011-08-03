
"""
ApiClient is a helper class to provide a base of functionality 
for all clients of the different types of API queries.
"""

import logging
import urllib2

USER_AGENT = "KBWCpy (0.1.0)"


class ApiClient:

    LOG = logging.getLogger("ApiClient")

    def __init__(self, institution_id, wskey, url_base, response_format="xml"):
        self.institution_id = institution_id
        self.wskey = wskey
        self.url_base = url_base
        self.response_format = response_format

    def _query_string(self, **kwargs):
        '''format the arguments into a query string'''
        q = '?'
        # Mostly this is here because "start-index" is unpythonic
        mapping = {'keyword': 'q',
                   'start_index': 'start-index',
                   'max_result': 'max-results',
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
        q += "wskey=%s&" % (self.wskey,)
        if self.response_format == "json":
            q += "alt=json&"
        return q.rstrip('&')

    def _get_response(self, query):
        self.LOG.info("Calling URL: %s" % (query,))
        headers = {'User-Agent': USER_AGENT}
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

    def _execute(self, query):
        pass
