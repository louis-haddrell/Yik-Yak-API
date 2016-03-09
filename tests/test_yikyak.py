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
        client = YikYak()

        # Mock response
        mock_request.return_value = {
            'ttl': 60,
            'pin': '123456',
        }

        # Assert PIN is returned
        pin = client.init_pairing("ABCDEFGHIJKLMNOPQRSTUVWXYZ012345")
        self.assertEqual(pin, '123456')

        # Assert _request() call is correct
        url = "https://www.yikyak.com/api/auth/initPairing"
        data = {'userID': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ012345'}
        mock_request.assert_called_with('POST', url, data=data)

    @mock.patch('yikyak.YikYak._request')
    def test_pair(self, mock_request):
        client = YikYak()

        # Mock response
        mock_request.return_value = 'auth_token'

        # Assert authentication token is returned
        token = client.pair('GBR', '1234567890', '123456')
        self.assertEqual(token, 'auth_token')

        # Assert API call is correct
        url = 'https://www.yikyak.com/api/auth/pair'
        json = {
            'countryCode': 'GBR',
            'phoneNumber': '1234567890',
            'pin': '123456',
        }

        mock_request.assert_called_with('POST', url, json=json)

    @mock.patch('yikyak.YikYak.pair')
    def test_login(self, mock_pair):
        """
        Assert .login() grabs the auth token

        Fail if the token is not assigned to YikYak.auth_token
        """
        mock_pair.return_value = "auth_token"

        client = YikYak()
        client.login("GBR", "1234567890", "123456")

        self.assertEqual(client.auth_token, "auth_token")
        mock_pair.assert_called_with("GBR", "1234567890", "123456")

    @mock.patch('yikyak.YikYak._get_yaks')
    def test_get_hot(self, mock_get):
        client = YikYak()
        client.get_hot(1, 2)
        mock_get.assert_called_with('hot', 1, 2)

    @mock.patch('yikyak.YikYak._get_yaks')
    def test_get_new(self, mock_get):
        client = YikYak()
        client.get_new(1, 2)
        mock_get.assert_called_with('new', 1, 2)

    def test_get_yaks_invalid(self):
        """
        Assert YikYak._get_yaks() throws an AssertionError if we attempt to
        retrieve from a feed that is not 'hot' or 'new'
        """
        client = YikYak()
        with self.assertRaises(AssertionError):
            client._get_yaks('abcd', 1, 2)

    @mock.patch('yikyak.YikYak._request')
    def test_compose_yak(self, mock_request):
        """
        Assert YikYak.compose_yak() makes the correct API call
        """
        client = YikYak()

        # Expected request
        url = "https://www.yikyak.com/api/proxy/v1/messages"
        params = {
            'lat': 50.93,
            'long': -1.76,
            'myHerd': 0,
            'userLat': 0,
            'userLong': 0,
        }
        json = {
            'handle': False,
            'message': 'Hello World',
        }

        yak = client.compose_yak("Hello World", 50.93, -1.76)
        self.assertTrue(isinstance(yak, Yak))
        mock_request.assert_called_with('POST', url, params=params, json=json)

    @mock.patch('yikyak.YikYak._request')
    def test_compose_yak_with_handle(self, mock_request):
        """
        Assert YikYak.compose_yak() makes the correct API call
        """
        client = YikYak()

        # Expected request
        url = "https://www.yikyak.com/api/proxy/v1/messages"
        params = {
            'lat': 50.93,
            'long': -1.76,
            'myHerd': 0,
            'userLat': 0,
            'userLong': 0,
        }
        json = {
            'handle': True,
            'message': 'Hello World',
        }

        yak = client.compose_yak("Hello World", 50.93, -1.76, handle=True)
        self.assertTrue(isinstance(yak, Yak))
        mock_request.assert_called_with('POST', url, params=params, json=json)

    @mock.patch('yikyak.YikYak._request')
    def test_get_yaks(self, mock_request):
        mock_request.return_value = []

        client = YikYak()
        client._get_yaks('hot', 50.93, -1.76)

        # Expected request
        url = 'https://www.yikyak.com/api/proxy/v1/messages/all/hot'
        params = {
            'userLat': 50.93,
            'userLong': -1.76,
            'lat': 50.93,
            'long': -1.76,
            'myHerd': 0,
        }

        mock_request.assert_called_with('GET', url, params=params)

    @mock.patch('yikyak.YikYak._request')
    def test_check_handle_availability_available(self, mock_request):
        """
        check_handle_availability() must return True for an available handle
        """
        mock_request.return_value = {'code': 0}

        client = YikYak()
        result = client.check_handle_availability('available')

        url = 'https://www.yikyak.com/api/proxy/v1/yakker/handles'
        params = {
            'handle': 'available',
        }
        mock_request.assert_called_with('GET', url, params=params)
        self.assertTrue(result)

    @mock.patch('yikyak.YikYak._request')
    def test_check_handle_availability_invalid(self, mock_request):
        """
        check_handle_availability() must return False for an invalid handle
        """
        mock_request.return_value = {'code': 1}

        client = YikYak()
        result = client.check_handle_availability('invalid')

        url = 'https://www.yikyak.com/api/proxy/v1/yakker/handles'
        params = {
            'handle': 'invalid',
        }
        mock_request.assert_called_with('GET', url, params=params)
        self.assertFalse(result)

    @mock.patch('yikyak.YikYak._request')
    def test_check_handle_availability_unavailable(self, mock_request):
        """
        check_handle_availability() must return False for an unavailable handle
        """
        mock_request.return_value = {'code': 2}

        client = YikYak()
        result = client.check_handle_availability('unavailable')

        url = 'https://www.yikyak.com/api/proxy/v1/yakker/handles'
        params = {
            'handle': 'unavailable',
        }
        mock_request.assert_called_with('GET', url, params=params)
        self.assertFalse(result)

    @mock.patch('yikyak.YikYak._request')
    def test_claim_handle(self, mock_request):
        mock_request.return_value = {'code': 0}

        client = YikYak()
        client.claim_handle('YikYakBot')
        url = 'https://www.yikyak.com/api/proxy/v1/yakker/handles'
        json = {
            'handle': 'YikYakBot',
        }
        mock_request.assert_called_with('POST', url, json=json)
