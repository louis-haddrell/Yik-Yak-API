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

    @mock.patch('yikyak.YikYak.pair')
    def test_login(self, mock_pair):
        """
        Assert .login() grabs the auth token

        Fail if the token is not assigned to YikYak.auth_token
        """
        mock_pair.return_value = "auth_token"

        yakker = YikYak()
        yakker.login("GBR", "1234567890", "123456")

        self.assertEqual(yakker.auth_token, "auth_token")
        mock_pair.assert_called_with("GBR", "1234567890", "123456")

    @mock.patch('yikyak.YikYak._get_yaks')
    def test_get_hot(self, mock_get):
        yakker = YikYak()
        yakker.get_hot(1, 2)
        mock_get.assert_called_with('hot', 1, 2)

    @mock.patch('yikyak.YikYak._get_yaks')
    def test_get_new(self, mock_get):
        yakker = YikYak()
        yakker.get_new(1, 2)
        mock_get.assert_called_with('new', 1, 2)

    def test_get_yaks_invalid(self):
        """
        Assert YikYak._get_yaks() throws an AssertionError if we attempt to
        retireve from a feed that is not 'hot' or 'new'
        """
        yakker = YikYak()
        with self.assertRaises(AssertionError):
            yakker._get_yaks('abcd', 1, 2)


if __name__ == "__main__":
    unittest.main()
