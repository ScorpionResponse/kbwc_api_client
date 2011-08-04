
from ApiClient import HttpApiClient
import logging


class OpenURL(HttpApiClient):

    def __init__(self, institution_id, wskey, url_base, response_format="xml"):
        HttpApiClient.__init__(self, institution_id, wskey, url_base, response_format)

    def openurl_query(self, **kwargs):
        pass
