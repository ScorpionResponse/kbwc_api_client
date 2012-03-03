'''
An implementation of a REST API client for the KB.
'''

from .ApiClient import HttpApiClient
from .util.xml2obj import xml2obj
import json


class Rest(HttpApiClient):
    '''Basic REST API that directly maps functions to most common KB queries'''

    def __init__(self, institution_id, wskey, url_base="http://worldcat.org/webservices/kb/", response_format="xml"):
        HttpApiClient.__init__(self, institution_id, wskey, url_base, response_format)

    def get_settings(self, **kwargs):
        '''Return the settings for this institution and only this institution.'''
        query_url = self.url_base + 'rest/settings/' + str(self.institution_id)
        params = self.create_query_params()
        return self.execute_query(query_url, params)

    def get_provider(self, provider_uid):
        '''Retrieve a record for a single provider by its identifier.'''
        query_url = self.url_base + 'rest/providers/' + str(provider_uid)
        params = self.create_query_params()
        return self.execute_query(query_url, params)

    def list_providers(self, start_index=1, max_results=10, order_by='title', **kwargs):
        '''List all providers configured for this institution.'''
        query_url = self.url_base + 'rest/providers'
        params = self.create_query_params(start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url, params)

    def search_providers(self, keyword=None, title=None, start_index=1, max_results=10, order_by='title', **kwargs):
        '''Search all providers configured for this institution.'''
        query_url = self.url_base + 'rest/providers/search'
        params = self.create_query_params(keyword=keyword, title=title, start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url, params)

    def get_collection(self, collection_uid):
        '''Retrieve a record for a single collection by its identifier.'''
        query_url = self.url_base + 'rest/collections/' + str(collection_uid)
        params = self.create_query_params()
        return self.execute_query(query_url, params)

    def list_collections(self, start_index=1, max_results=10, order_by='title', **kwargs):
        '''List all collections configured for this institution.'''
        query_url = self.url_base + 'rest/collections'
        params = self.create_query_params(start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url, params)

    def search_collections(self, keyword=None, title=None, collection_uid=None, provider_uid=None, start_index=1, max_results=10, order_by='title', **kwargs):
        '''Search all collections configured for this institution.'''
        query_url = self.url_base + 'rest/collections/search'
        params = self.create_query_params(keyword=keyword, title=title, collection_uid=collection_uid, provider_uid=provider_uid, start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url, params)

    def get_entry(self, entry_id):
        '''Retrieve a record for a single entry (title) by its identifier.'''
        query_url = self.url_base + 'rest/entries/' + str(entry_id)
        params = self.create_query_params()
        return self.execute_query(query_url, params)

    def list_entries(self, start_index=1, max_results=10, order_by='title', **kwargs):
        '''List all entries configured for this institution.'''
        query_url = self.url_base + 'rest/entries'
        params = self.create_query_params(start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url, params)

    def search_entries(self, keyword=None, title=None, collection_uid=None, provider_uid=None, issn=None, isbn=None, oclcnum=None, content=None, start_index=1, max_results=10, order_by='title', **kwargs):
        '''Search all entries configured for this collection.'''
        query_url = self.url_base + 'rest/entries/search'
        params = self.create_query_params(keyword=keyword, title=title, collection_uid=collection_uid, provider_uid=provider_uid, content=content, start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url, params)

    def browse_entries(self, title=None, content=None, start_index=1, max_results=10, order_by='title', **kwargs):
        '''Browse the entries configured for this institution.

           This is the query to use to build an A to Z list.
        '''
        if title is not None:
            title = '"' + title + '%"'
        kwargs["search_type"] = "atoz"
        query_url = self.url_base + 'rest/entries/search'
        params = self.create_query_params(title=title, content=content, start_index=start_index, max_results=max_results, order_by=order_by, **kwargs)
        return self.execute_query(query_url, params)

    def create_query_params(self, **kwargs):
        '''Format the arguments into a query string.

           Certain arguments are rewritten slightly to use the API conventions.
           institution_id and wskey are always added.
        '''
        payload = {}
        # Mostly this is here because "start-index" is unpythonic
        mapping = {'keyword': 'q',
                   'start_index': 'start-index',
                   'max_results': 'max-results',
                   'order_by': 'order-by'}
        for i in kwargs:
            if kwargs[i] is not None:
                if i in mapping:
                    payload[mapping[i]] = kwargs[i]
                else:
                    payload[i] = kwargs[i]
        payload['institution_id'] = self.institution_id
        if self.wskey:
            payload['wskey'] = self.wskey
        payload['alt'] = self.response_format
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
        '''Reformat the JSON response to match the XML.'''
        self.LOG.debug("JSON Data from server: %s" % (jsondata,))
        d = json.loads(jsondata, encoding="UTF-8")
        ref = None
        if 'entries' in d:
            # if entries in the json then we're dealing with a multi-result response
            ref = d
        else:
            # It looks like single responses aren't lists of 1 like the XML version
            ref = [d]
        self.LOG.debug("JSON Data reformatted: %s" % (ref,))
        return ref

    def _xml_reformat(self, xmldata):
        '''Reformat the XML response.'''
        self.LOG.debug("XML Data from server: %s" % (xmldata,))
        obj = xml2obj(xmldata.encode('utf-8'))
        d = obj.get_result()

        ref = None
        if 'entry' in d.keys():
            ref = d
            if isinstance(ref['entry'], list):
                ref['entries'] = ref['entry']
            else:
                ref['entries'] = [ref['entry']]
            del ref['entry']
        else:
            del d[u'xmlns']
            del d[u'xmlns:kb']
            d[u'title'] = d[u'title'][u'data']
            d[u'links'] = d[u'link']
            del d[u'link']
            ref = [d]

        self.LOG.debug("XML Data reformatted: %s" % (ref,))
        return ref
