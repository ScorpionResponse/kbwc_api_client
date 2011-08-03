
from ApiClient import ApiClient
import logging

class OpenURL(ApiClient):

    def __init__(self, institution_id, wskey, url_base, response_format="xml"):
        ApiClient.__init__(self, institution_id, wskey, url_base, response_format)

    def openurl_query(self, **kwargs):
        pass
