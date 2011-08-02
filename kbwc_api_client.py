#!/usr/bin/env python

import feedparser
import simplejson
import sys
import urllib2

USER_AGENT = "KBWCpy (v1)"


class kbwc_api_client:

    def __init__(self, institution_id, wskey, url_base, response_format="xml"):
        self.institution_id = institution_id
        self.wskey = wskey
        self.url_base = url_base
        self.response_format = response_format

    def openurl(self, **kwargs):
        pass

    def get_settings(self, **kwargs):
        query_url = self.url_base + 'rest/settings/' + str(self.institution_id) + self._query_string()
        return self._execute(query_url)

    def get_provider(self, provider_uid):
        query_url = self.url_base + 'rest/providers/' + urllib2.quote(provider_uid) + self._query_string()
        return self._execute(query_url)

    def list_providers(self, start_index=1, max_result=10, order_by='title', **kwargs):
        query_url = self.url_base + 'rest/providers' + self._query_string(start_index=start_index, max_result=max_result, order_by=order_by, **kwargs)
        return self._execute(query_url)

    def search_providers(self, keyword=None, title=None, start_index=1, max_result=10, order_by='title', **kwargs):
        query_url = self.url_base + 'rest/providers/search' + self._query_string(keyword=keyword, title=title, start_index=start_index, max_result=max_result, order_by=order_by, **kwargs)
        return self._execute(query_url)

    def get_collection(self, collection_uid):
        query_url = self.url_base + 'rest/collections/' + urllib2.quote(collection_uid) + self._query_string()
        return self._execute(query_url)

    def list_collections(self, start_index=1, max_result=10, order_by='title', **kwargs):
        query_url = self.url_base + 'rest/collections' + self._query_string(start_index=start_index, max_result=max_result, order_by=order_by, **kwargs)
        return self._execute(query_url)

    def search_collections(self, keyword=None, title=None, collection_uid=None, provider_uid=None, start_index=1, max_result=10, order_by='title', **kwargs):
        query_url = self.url_base + 'rest/collections/search' + self._query_string(keyword=keyword, title=title, collection_uid=collection_uid, provider_uid=provider_uid, start_index=start_index, max_result=max_result, order_by=order_by, **kwargs)
        return self._execute(query_url)

    def get_entry(self, entry_id):
        query_url = self.url_base + 'rest/entries/' + urllib2.quote(entry_id) + self._query_string()
        return self._execute(query_url)

    def list_entries(self, start_index=1, max_result=10, order_by='title', **kwargs):
        query_url = self.url_base + 'rest/entries' + self._query_string(start_index=start_index, max_result=max_result, order_by=order_by, **kwargs)
        return self._execute(query_url)

    def search_entries(self, keyword=None, title=None, collection_uid=None, provider_uid=None, issn=None, isbn=None, oclcnum=None, content=None, start_index=1, max_result=10, order_by='title', **kwargs):
        query_url = self.url_base + 'rest/entries/search' + self._query_string(keyword=keyword, title=title, collection_uid=collection_uid, provider_uid=provider_uid, content=content, start_index=start_index, max_result=max_result, order_by=order_by, **kwargs)
        return self._execute(query_url)

    def browse_entries(self, title=None, content=None, start_index=1, max_result=10, order_by='title', **kwargs):
        if title is not None:
            title = '"' + title + '%"'
        kwargs["search_type"] = "atoz"
        query_url = self.url_base + 'rest/entries/search' + self._query_string(title=title, content=content, start_index=start_index, max_result=max_result, order_by=order_by, **kwargs)
        return self._execute(query_url)

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

    def _execute(self, query):
        print "Calling URL: %s" % (query,)
        headers = {'User-Agent': USER_AGENT}
        request = urllib2.Request(query, headers=headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            sys.stderr.write("Status code %s from URL '%s'\n" % (e.code, query))
            return None
        except urllib2.URLError, e:
            sys.stderr.write("Problem making the requests for URL '%s'. Exception: %s\n" % (query, e))
            return None
        sys.stderr.write("Status code %s from URL '%s'\n" % (response.code, query))

        if self.response_format == "json":
            d = simplejson.load(response, encoding="UTF-8")
            return self._json_reformat(d)
        else:
            d = feedparser.parse(response)
            if d.bozo:
                # 'bozo' is set by feedparser if the XML does not parse correctly
                sys.stderr.write("%s - %s\n" % (d.bozo_exception.getLineNumber(), d.bozo_exception.getMessage()))
                print d
            return self._xml_reformat(d)
        return None

if __name__ == '__main__':
    inst_id = 6569
    wskey = '4QpcmGhh34L7LLeo7p5PNJAsz14fQtyihkeGSgEUVFB33EWkocQ3JnNQ5A6wvzKAYxRYokTzeIFdOvG4'
    url_base = 'http://kbwcap02dxdu.dev.oclc.org:8080/kbwc-grid/'
    #url_base = 'http://kbwcperf.ent.oclc.org:8080/webservices/kb/'
    #client = kbwc_api_client(inst_id, wskey, url_base, "json")
    client = kbwc_api_client(inst_id, wskey, url_base)

    from pprint import pprint
    #pprint(client.get_settings())
    #pprint(client.get_provider('NPG'))
    # #pprint(client.search_entries(title='"N"'))
    #pprint(client.list_providers())
    #pprint(client.search_providers('Nature'))
    #pprint(client.get_collection('NPG.journals'))
    #pprint(client.list_collections())
    #pprint(client.search_collections('Nature'))
    #pprint(client.get_entry('036f688a982b7a702aadd05003f9742e'))
    #pprint(client.get_entry('NPG.journals,1987357'))
    #pprint(client.list_entries())
    #pprint(client.search_entries('Nature'))
    #pprint(client.browse_entries())
    pprint(client.browse_entries('n'))
