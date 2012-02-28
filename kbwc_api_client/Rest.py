'''
An implementation of a REST API client for the KB.
'''

from ApiClient import HttpApiClient
import logging
try:
    import json
except ImportError:
    import simplejson as json
import urllib2
from util.xml2obj import xml2obj


class Rest(HttpApiClient):
    '''Basic REST API that directly maps functions to most common KB queries'''

    LOG = logging.getLogger("Rest")

    def __init__(self, institution_id, wskey, url_base="http://worldcat.org/webservices/kb/", response_format="xml"):
        HttpApiClient.__init__(self, institution_id, wskey, url_base, response_format)

    def get_settings(self, **kwargs):
        '''Return the settings for this institution and only this institution.'''
        query_url = self.url_base + 'rest/settings/' + str(self.institution_id) + self.create_query_string()
        return self.execute_query(query_url)

    def get_provider(self, provider_uid):
        '''Retrieve a record for a single provider by its identifier.'''
        query_url = self.url_base + 'rest/providers/' + urllib2.quote(provider_uid) + self.create_query_string()
        return self.execute_query(query_url)

    def list_providers(self, start_index=1, max_results=10, order_by='title', **kwargs):
        '''List all providers configured for this institution.'''
        query_url = self.url_base + 'rest/providers' + self.create_query_string(start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url)

    def search_providers(self, keyword=None, title=None, start_index=1, max_results=10, order_by='title', **kwargs):
        '''Search all providers configured for this institution.'''
        query_url = self.url_base + 'rest/providers/search' + self.create_query_string(keyword=keyword, title=title, start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url)

    def get_collection(self, collection_uid):
        '''Retrieve a record for a single collection by its identifier.'''
        query_url = self.url_base + 'rest/collections/' + urllib2.quote(collection_uid) + self.create_query_string()
        return self.execute_query(query_url)

    def list_collections(self, start_index=1, max_results=10, order_by='title', **kwargs):
        '''List all collections configured for this institution.'''
        query_url = self.url_base + 'rest/collections' + self.create_query_string(start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url)

    def search_collections(self, keyword=None, title=None, collection_uid=None, provider_uid=None, start_index=1, max_results=10, order_by='title', **kwargs):
        '''Search all collections configured for this institution.'''
        query_url = self.url_base + 'rest/collections/search' + self.create_query_string(keyword=keyword, title=title, collection_uid=collection_uid, provider_uid=provider_uid, start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url)

    def get_entry(self, entry_id):
        '''Retrieve a record for a single entry (title) by its identifier.'''
        query_url = self.url_base + 'rest/entries/' + urllib2.quote(entry_id) + self.create_query_string()
        return self.execute_query(query_url)

    def list_entries(self, start_index=1, max_results=10, order_by='title', **kwargs):
        '''List all entries configured for this institution.'''
        query_url = self.url_base + 'rest/entries' + self.create_query_string(start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url)

    def search_entries(self, keyword=None, title=None, collection_uid=None, provider_uid=None, issn=None, isbn=None, oclcnum=None, content=None, start_index=1, max_results=10, order_by='title', **kwargs):
        '''Search all entries configured for this collection.'''
        query_url = self.url_base + 'rest/entries/search' + self.create_query_string(keyword=keyword, title=title, collection_uid=collection_uid, provider_uid=provider_uid, content=content, start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url)

    def browse_entries(self, title=None, content=None, start_index=1, max_results=10, order_by='title', **kwargs):
        '''Browse the entries configured for this institution.

           This is the query to use to build an A to Z list.
        '''
        if title is not None:
            title = '"' + title + '%"'
        kwargs["search_type"] = "atoz"
        query_url = self.url_base + 'rest/entries/search' + self.create_query_string(title=title, content=content, start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url)

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
        elif self.response_format == "xml":
            q += "alt=xml&"
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
        '''Reformat the JSON response to match the XML.'''
        self.LOG.debug("JSON Data from server: %s" % (jsondata,))
        ref = None
        if 'entries' in jsondata:
            # if entries in the json then we're dealing with a multi-result response
            ref = jsondata
        else:
            # It looks like single responses aren't lists of 1 like the XML version
            ref = [jsondata]
        self.LOG.debug("JSON Data reformatted: %s" % (ref,))
        return ref

    def _xml_reformat(self, xmldata):
        '''Reformat the XML response.  This mostly removes some junk feedparser stuck in there'''
        self.LOG.debug("XML Data from server: %s" % (xmldata,))

        ref = None
        if 'entry' in xmldata.keys():
            ref = xmldata
            if isinstance(ref['entry'], list):
                ref['entries'] = ref['entry']
            else:
                ref['entries'] = [ref['entry']]
            del ref['entry']
            #    if k.startswith('os_'):
            #        new_k = 'os:' + k[3:]
            #        ref[new_k] = v
            #        del ref[k]
        else:
            del xmldata[u'xmlns']
            del xmldata[u'xmlns:kb']
            xmldata[u'title'] = xmldata[u'title'][u'data']
            xmldata[u'links'] = xmldata[u'link']
            del xmldata[u'link']
            ref = [xmldata]

        self.LOG.debug("XML Data reformatted: %s" % (ref,))
        return ref
