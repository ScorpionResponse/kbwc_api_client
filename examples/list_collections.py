#!/usr/bin/env python

import kbwc_api_client
from pprint import pprint
import logging

def main(resp_form="xml"):
    print "Getting response in format: %s" % (resp_form,)
    #inst_id = 111637
    inst_id = 6569
    wskey = 'TjBKm4f7QdZwxUrvfnukshyAIPkCgt3ZieslDR23Z95rV8rmqU3gIFvKRRDaTwX4UwzoQtQYIbyCqEWe'
    client = kbwc_api_client.Rest(inst_id, wskey, response_format=resp_form)
    response = client.list_collections()
    print "Response: " 
    pprint(response)

if __name__ == '__main__':
    LOG = logging.getLogger()
    LOG.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    LOG.addHandler(ch)
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
