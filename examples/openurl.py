#!/usr/bin/env python

import kbwc_api_client
import logging
from pprint import pprint

def main():
    #resp_form = 'xml'
    resp_form = 'json'
    inst_id = 111637
    wskey = 'TjBKm4f7QdZwxUrvfnukshyAIPkCgt3ZieslDR23Z95rV8rmqU3gIFvKRRDaTwX4UwzoQtQYIbyCqEWe'
    client = kbwc_api_client.OpenURL(inst_id, wskey, response_format=resp_form)
    response = client.openurl_query(title="Discrete Dynamics in Nature and Society", content='fulltext', collection_uid="hindawi.journals", doi="10.1155/2011/516418", date='2011', volume='2011')
    print "Response: " 
    pprint(response)


if __name__ == '__main__':
    LOG = logging.getLogger()
    LOG.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    #ch.setLevel(logging.INFO)
    LOG.addHandler(ch)
    main()
