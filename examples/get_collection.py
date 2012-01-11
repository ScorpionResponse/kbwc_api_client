#!/usr/bin/env python

import kbwc_api_client
from pprint import pprint

def main(collection_uid, resp_form="xml"):
    print "Looking up collection info by ID: %s" % (collection_uid,)
    print "Getting response in format: %s" % (resp_form,)
    inst_id = 111637
    wskey = 'TjBKm4f7QdZwxUrvfnukshyAIPkCgt3ZieslDR23Z95rV8rmqU3gIFvKRRDaTwX4UwzoQtQYIbyCqEWe'
    client = kbwc_api_client.Rest(inst_id, wskey, response_format=resp_form)
    response = client.get_collection(collection_uid)
    print "Response: " 
    pprint(response)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s collection_uid [format]\n" % (sys.argv[0],))
        sys.exit()
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        main(sys.argv[1])
