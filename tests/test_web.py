import json
import unittest
from unittest import mock

from yikyakapi.web import WebObject


class TestSuite(unittest.TestCase):
    def test_base_url(self):
        """WebObject should include the base URL variable"""
        web = WebObject()
        self.assertEqual(web.base_url, "https://www.yikyak.com/api/v2/")

    def test_session(self):
        """Ensure the session object is initialised correctly"""
        web = WebObject()
        self.assertEqual(web.session.headers['Referer'], 'https://yikyak.com')
        self.assertNotIn('User-Agent', web.session.headers)

    def test__request(self):
        """Assert ._request uses session object to make requests"""
        web = WebObject()
        mock_response = mock.Mock()
        mock_response.json.return_value = {}
        web.session = mock.Mock()
        web.session.request.return_value = mock_response

        web._request('GET', 'http://yikyak.com')
        web.session.request.assert_called_with('GET', 'http://yikyak.com')

    def test_request_invalid_json(self):
        """
        Assert that _request() will still work if a JSONDecodeError occurs

        Exception should result in an empty dict being returned
        """
        # Mock response object
        mock_response = mock.Mock()
        mock_response.json.side_effect = json.decoder.JSONDecodeError('', '', 0)

        web = WebObject()
        web.session = mock.Mock()
        web.session.request.return_value = mock_response

        response = web._request('', '')
        self.assertEqual(response, {})

    @mock.patch('yikyakapi.web.WebObject._request')
    def test_refresh_token(self, mock_request):
        mock_request.return_value = 'new_token'

        web = WebObject()
        web.refresh_token()

        url = 'https://www.yikyak.com/api/auth/token/refresh'
        mock_request.assert_called_with('POST', url)

        self.assertEqual(web.session.headers['x-access-token'], 'new_token')
