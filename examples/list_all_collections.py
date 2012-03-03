#!/usr/bin/env python

import kbwc_api_client
#from pprint import pprint
import logging

def list_all_collections(kbwc_client):
    collection_list = []
    start_index = 1
    total_results = 2
    while total_results > start_index:
        response = kbwc_client.list_collections(start_index=start_index)
        print response
        total_results = int(response['os:totalresults'])
        response_size = int(response['os:itemsperpage'])
        collection_list.extend(response['entries'])
        start_index = start_index + response_size
    return collection_list

def collections_print(collections):
    columns = ['kb:owner_institution', 'kb:provider_uid', 'kb:provider_name', 'kb:collection_uid', 'title', 'kb:selected_entries', 'kb:available_entries']
    print '\t'.join(columns)
    for i, coll in enumerate(collections):
        row = ''
        for c in columns:
            if c in coll:
                row += coll[c] + '\t'
            else:
                row += '\t'
        print row[0:-1]

def main(inst_id):
    resp_form = 'xml'
    #print "Getting response in format: %s" % (resp_form,)
    #inst_id = 111637
    #inst_id = 6569
    #wskey = 'TjBKm4f7QdZwxUrvfnukshyAIPkCgt3ZieslDR23Z95rV8rmqU3gIFvKRRDaTwX4UwzoQtQYIbyCqEWe'
    wskey = None
    client = kbwc_api_client.Rest(inst_id, wskey, url_base="http://worldcat.org/webservices/kb/", response_format=resp_form)
    collections = list_all_collections(client)
    collections_print(collections)
    #response = client.list_collections()
    #print "Response: " 
    #pprint(response)

if __name__ == '__main__':
    LOG = logging.getLogger()
    #LOG.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    LOG.addHandler(ch)
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.stderr.write("Usage: %s <institution_id>\n" % (sys.argv[0],))
        sys.exit()
