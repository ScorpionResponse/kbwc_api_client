===========
kbwc_api_client
===========

kbwc_api_client is a basic client for interacting with the API for the 
WorldCat knowledge base.

http://oclc.org/knowledgebase

The client should support both JSON and XML format responses.  The responses
are both returned as python objects with largely the same structure for client
code to use either fairly transparently.

* Note that JSON is not fully supported in the current production KB API, so 
  the client will raise an exception if it is used at this time.
