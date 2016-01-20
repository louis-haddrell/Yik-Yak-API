import requests

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

        response = requests.request(method, url, **kwargs)
        response.raise_for_status()

        try:
            return response.json()
        except JSONDecodeError:
            return {}

    def refresh_token(self):
        """
        Refresh the auth token
        """
        url = 'https://yikyak.com/api/auth/token/refresh'
        self.auth_token = self._request('POST', url)
