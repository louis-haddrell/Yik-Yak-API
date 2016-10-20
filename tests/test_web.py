import json
import unittest
from unittest import mock

from yikyakapi.web import *


class TestSuite(unittest.TestCase):
    def test_base_url(self):
        """WebObject should include the base URL variable"""
        web = WebObject()
        self.assertEqual(web.base_url, "https://www.yikyak.com/api/v2/")

    @mock.patch('yikyakapi.web.requests.request')
    def test_request_headers(self, mock_request):
        """Assert standard headers are sent in the request"""
        mock_response = mock.Mock()
        mock_request.return_value = mock_response
        mock_response.json.return_value = {}

        web = WebObject()
        web.auth_token = 'auth_token'

        method = 'GET'
        url = 'http://yikyak.com'
        headers = {
            'Referer': 'https://yikyak.com/',
            'x-access-token': 'auth_token',
        }

        web._request(method, url)
        mock_request.assert_called_with(method, url, headers=headers)

    @mock.patch('yikyakapi.web.requests')
    def test_request_invalid_json(self, mock_request):
        """
        Assert that _request() will still work if a JSONDecodeError occurs

        Exception should result in an empty dict being returned
        """
        # Mock response object
        mock_response = mock.Mock()
        mock_response.json.side_effect = json.decoder.JSONDecodeError('', '', 0)
        mock_request.request.return_value = mock_response

        web = WebObject()
        response = web._request('', '')
        self.assertEqual(response, {})

    @mock.patch('yikyakapi.web.WebObject._request')
    def test_refresh_token(self, mock_request):
        mock_request.return_value = 'new_token'

        web = WebObject()
        web.auth_token = 'old_token'
        web.refresh_token()

        self.assertEqual(web.auth_token, 'new_token')

        url = 'https://www.yikyak.com/api/auth/token/refresh'
        mock_request.assert_called_with('POST', url)
