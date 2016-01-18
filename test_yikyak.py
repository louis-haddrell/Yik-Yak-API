import json
import unittest
from unittest import mock

from yikyak import *


class TestSuite(unittest.TestCase):
    @mock.patch('yikyak.YikYak._request')
    def test_init_pairing(self, mock_request):
        """
        Assert init_pairing() makes API call to retrieve auth PIN
        """
        yakker = YikYak()

        # Mock response
        mock_request.return_value = {
            'ttl': 60,
            'pin': '123456',
        }

        # Assert PIN is returned
        pin = yakker.init_pairing("ABCDEFGHIJKLMNOPQRSTUVWXYZ012345")
        self.assertEqual(pin, '123456')

        # Assert _request() call is correct
        url = "https://beta.yikyak.com/api/auth/initPairing"
        data = {'userID': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ012345'}
        mock_request.assert_called_with('POST', url, data=data)

    @mock.patch('yikyak.YikYak._request')
    def test_pair(self, mock_request):
        yakker = YikYak()

        # Mock response
        mock_request.return_value = 'auth_token'

        # Assert authentication token is returned
        token = yakker.pair('GBR', '1234567890', '123456')
        self.assertEqual(token, 'auth_token')

        # Assert API call is correct
        url = 'https://beta.yikyak.com/api/auth/pair'
        headers = {'Referer': 'https://beta.yikyak.com/'}
        json = {
            'countryCode': 'GBR',
            'phoneNumber': '1234567890',
            'pin': '123456',
        }

        mock_request.assert_called_with('POST', url, headers=headers, json=json)

    @mock.patch('yikyak.YikYak._request')
    def test_upvote(self, mock_request):
        # Mock Yak
        mock_yak = mock.Mock()
        mock_yak.messageID = 'R/abcdef0123456789abcdef0123456'
        mock_yak.latitude = 50.93
        mock_yak.longitude = -1.76

        # Set up YikYak
        yakker = YikYak()
        yakker.auth_token = 'auth_token'
        yakker.upvote(mock_yak)

        # Assert API call is correct
        url = 'https://beta.yikyak.com/api/proxy/v1/messages/R%2Fabcdef0123456789abcdef0123456/upvote'

        headers = {
            'Referer': 'https://beta.yikyak.com/',
            'x-access-token': 'auth_token',
        }

        params = {
            'userLat': 50.93,
            'userLong': -1.76,
            'myHerd': 0,
        }

        mock_request.assert_called_with('PUT', url, headers=headers, params=params)

    @mock.patch('yikyak.YikYak._request')
    def test_downvote(self, mock_request):
        # Mock Yak
        mock_yak = mock.Mock()
        mock_yak.messageID = 'R/abcdef0123456789abcdef0123456'
        mock_yak.latitude = 50.93
        mock_yak.longitude = -1.76

        # Set up YikYak
        yakker = YikYak()
        yakker.auth_token = 'auth_token'
        yakker.downvote(mock_yak)

        # Assert API call is correct
        url = 'https://beta.yikyak.com/api/proxy/v1/messages/R%2Fabcdef0123456789abcdef0123456/downvote'

        headers = {
            'Referer': 'https://beta.yikyak.com/',
            'x-access-token': 'auth_token',
        }

        params = {
            'userLat': 50.93,
            'userLong': -1.76,
            'myHerd': 0,
        }

        mock_request.assert_called_with('PUT', url, headers=headers, params=params)        

    @mock.patch('yikyak.requests')
    def test_request_invalid_json(self, mock_request):
        """
        Assert that _request() will still work if a JSONDecodeError occurs

        Exception should result in an empty dict being returned
        """
        # Mock response object
        mock_response = mock.Mock()
        mock_response.json.side_effect = json.decoder.JSONDecodeError('', '', 0)
        mock_request.request.return_value = mock_response

        yakker = YikYak()
        response = yakker._request('', '')
        self.assertEqual(response, {})


if __name__ == "__main__":
    unittest.main()
