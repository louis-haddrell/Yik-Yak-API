import json
import unittest
from unittest import mock

from web import *


class TestSuite(unittest.TestCase):
    @mock.patch('web.requests')
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
