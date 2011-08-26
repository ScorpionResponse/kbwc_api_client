'''
An implementation of a REST API client for the KB.
'''

from ApiClient import HttpApiClient
import feedparser
import logging
import simplejson
import urllib2


class Rest(HttpApiClient):
    '''Basic REST API that directly maps functions to most common KB queries'''

    LOG = logging.getLogger("Rest")

    def __init__(self, institution_id, wskey, url_base, response_format="xml"):
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

    def execute_query(self, query):
        '''Calls the api with a particular query string and does some basic response parsing.'''
        response = self.get_response(query)
        if response is None:
            return None
        self.LOG.debug("Response: %s" % (response,))
        if self.response_format == "json":
            d = simplejson.load(response, encoding="UTF-8")
            return self._json_reformat(d)
        else:
            d = feedparser.parse(response)
            if d.bozo:
                # 'bozo' is set by feedparser if the XML does not parse correctly
                self.LOG.warn("%s - %s\n" % (d.bozo_exception.getLineNumber(), d.bozo_exception.getMessage()))
                self.LOG.debug(d)
            return self._xml_reformat(d)
        return None

    def _json_reformat(self, jsondata):
        '''Reformat the JSON response to match the XML.'''
        ref = None
        if 'entries' in jsondata:
            # skipping to entries means we lose the counts in the response.  probably should not do that
            ref = jsondata['entries']
        else:
            # It looks like single responses aren't lists of 1 like the XML version
            ref = [jsondata]

        for i in ref:
            # Turn all 'extensions' into top level keys in the dict
            for j in i['extensions']:
                name = j['name']
                if name.startswith("kb:"):
                    # feedparser uses _ instead of : so emulate that
                    name = "kb_" + name[3:]
                val = j['children']
                # Assume all children have either zero or one value
                if len(val) == 1:
                    val = val[0]
                elif len(val) == 0:
                    val = ''
                i[name] = val.rstrip()
            del i['extensions']

        return ref

    def _xml_reformat(self, xmldata):
        '''Reformat the XML response.  This mostly removes some junk feedparser stuck in there'''
        # feedparser was probably a bad choice
        # skipping to entries means we lose the counts in the response.  probably should not do that
        ref = xmldata.entries
        for i in ref:
            # title_detail added by feedparser
            del i['title_detail']
            for l in i['links']:
                # type added by feedparser
                del l['type']
                # do this to counteract the relative link processing
                if l['rel'] == 'via' and 'href' in l and l['href'].startswith(self.url_base):
                    l['href'] = ''
            # According to the feedparser docs, this should not happen.  I believe it happens with:
            # <link rel="via"/>
            if 'link' in i:
                del i['link']
        return ref
