import logging
import requests

from json import dumps as json_dumps
from json.decoder import JSONDecodeError


class WebObject(object):
    def __init__(self):
        self.auth_token = None

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
        # Standard auth headers
        auth_headers = {
            'Referer': 'https://yikyak.com/',
            'x-access-token': self.auth_token,
        }

        # Retrieve custom headers (if any) from kwargs
        headers = kwargs.get('headers', {})

        # Give custom headers priority
        auth_headers.update(headers)

        # Place back in kwargs
        kwargs['headers'] = auth_headers

        logging.debug(method)
        logging.debug(url)
        logging.debug(kwargs)

        response = requests.request(method, url, **kwargs)

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
        self.auth_token = self._request('POST', url)
