import logging
import requests

from json import dumps as json_dumps
from json.decoder import JSONDecodeError


class WebObject(object):
    def __init__(self):
        self.auth_token = None
        self.base_url = "https://www.yikyak.com/api/v2/"

        self.session = requests.Session()
        self.session.headers.update({'Referer': 'https://yikyak.com'})

    def _request(self, method, url, **kwargs):
        """
        Wrapper for requests.request()

        Performs the following additional functions:
            - Automatically includes required auth headers
            - Throws errors for non-200 HTTP status codes
            - Handles invalid JSON responses

        Arguments:
            method (string): HTTP method
            url (string): URL to make the request to
            **kwargs: any kwargs allowed by requests.request()
        """
        logging.debug(method)
        logging.debug(url)
        logging.debug(kwargs)

        response = self.session.request(method, url, **kwargs)

        try:
            json = response.json()
        except JSONDecodeError:
            logging.warning("Failed to decode JSON from response")
            json = {}

        logging.debug(json_dumps(json, indent=4))
        response.raise_for_status()
        return json

    def refresh_token(self):
        """
        Refresh the auth token
        """
        url = 'https://www.yikyak.com/api/auth/token/refresh'
        auth_token = self._request('POST', url)
        self.session.headers.update({'x-access-token': auth_token})
