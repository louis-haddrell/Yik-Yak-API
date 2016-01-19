import requests

from json.decoder import JSONDecodeError


class WebObject(object):
    def __init__(self):
        self.auth_token = None

    def _request(self, method, url, **kwargs):
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()

        try:
            return response.json()
        except JSONDecodeError:
            return {}
