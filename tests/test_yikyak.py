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
        url = "https://yikyak.com/api/auth/initPairing"
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
        url = 'https://yikyak.com/api/auth/pair'
        headers = {'Referer': 'https://yikyak.com/'}
        json = {
            'countryCode': 'GBR',
            'phoneNumber': '1234567890',
            'pin': '123456',
        }

        mock_request.assert_called_with('POST', url, headers=headers, json=json)

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

    @mock.patch('yikyak.YikYak._request')
    def test_compose_yak(self, mock_request):
        yakker = YikYak()
        yakker.auth_token = 'auth_token'

        # Expected request
        url = "https://yikyak.com/api/proxy/v1/messages"
        headers = {
            'Referer': 'https://yikyak.com/',
            'x-access-token': 'auth_token',
        }
        params = {
            'lat': 50.93,
            'long': -1.76,
            'myHerd': 0,
            'userLat': 0,
            'userLong': 0,
        }
        json = {
            'message': 'Hello World',
        }

        yakker.compose_yak("Hello World", 50.93, -1.76)
        mock_request.assert_called_with(
            'POST', url, headers=headers, params=params, json=json
        )


if __name__ == "__main__":
    unittest.main()
