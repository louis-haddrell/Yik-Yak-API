import json
import unittest
from unittest import mock

from yikyakapi.yikyak import *


class TestSuite(unittest.TestCase):
    @mock.patch('yikyakapi.yikyak.YikYak._request')
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

    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test_pair(self, mock_request):
        client = YikYak()

        # Mock response
        mock_request.return_value = 'token'

        # Assert authentication token is returned
        token = client.pair('GBR', '1234567890', '123456')
        self.assertEqual(token, 'token')

        # Assert API call is correct
        url = 'https://www.yikyak.com/api/auth/pair'
        json = {
            'countryCode': 'GBR',
            'phoneNumber': '1234567890',
            'pin': '123456',
        }

        mock_request.assert_called_with('POST', url, json=json)

    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test_pair_yakker(self, mock_request):
        """Cached yakker should be cleared on loging"""
        client = YikYak()
        client._yakker = mock.Mock()

        client.pair("GBR", "1234567890", "123456")

        self.assertEqual(client._yakker, None)

    @mock.patch('yikyakapi.yikyak.Yakker.refresh')
    @mock.patch('yikyakapi.yikyak.YikYak.get_csrf_token')
    @mock.patch('yikyakapi.yikyak.YikYak.pair')
    def test_login(self, mock_pair, mock_csrf, mock_yakker):
        """Assert .login() retrieves the access token and CSRF token"""
        mock_pair.return_value = "access_token"
        mock_csrf.return_value = "csrf_token"

        client = YikYak()
        client.session = mock.Mock()

        # Assert .pair() is called
        client.login("GBR", "1234567890", "123456")
        mock_pair.assert_called_with("GBR", "1234567890", "123456")
        mock_csrf.assert_called_with()

        headers = {
            'x-access-token': 'access_token',
            'X-Csrf-Token': 'csrf_token',
        }
        client.session.headers.update.assert_called_with(headers)

        mock_yakker.assert_called_with()

    def test_get_csrf_token(self):
        client = YikYak()

        html = "\"csrfToken\":\"ekyJ0Oht-HaDXAMs6fd_H1Qz-E7GZvNkAzS0\""
        response = mock.Mock()
        response.text = html

        client.session = mock.Mock()
        client.session.get.return_value = response

        token = client.get_csrf_token()
        self.assertEqual(token, 'ekyJ0Oht-HaDXAMs6fd_H1Qz-E7GZvNkAzS0')

    @mock.patch('yikyakapi.yikyak.YikYak.init_pairing')
    @mock.patch('yikyakapi.yikyak.YikYak.login')
    def test_login_id(self, mock_login, mock_init_pairing):
        mock_init_pairing.return_value = "123456"

        client = YikYak()
        client.login_id("GBR", "1234567890", "ABCDEFG")
        mock_login.assert_called_with("GBR", "1234567890", "123456")

    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test__get_yaks(self, mock_request):
        mock_request.return_value = []

        client = YikYak()
        client._get_yaks('https://www.yikyak.com/')

        # Expected request
        url = 'https://www.yikyak.com/'
        params = {
            'feedType': 'new',
            'lat': 0,
            'long': 0,
            'userLat': 0,
            'userLong': 0,
        }

        mock_request.assert_called_with('GET', url, params=params)

    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test__get_yaks_coords(self, mock_request):
        mock_request.return_value = []

        client = YikYak()
        client._get_yaks('https://www.yikyak.com/', 50.93, -1.76)

        # Expected request
        url = 'https://www.yikyak.com/'
        params = {
            'feedType': 'new',
            'lat': 50.93,
            'long': -1.76,
            'userLat': 50.93,
            'userLong': -1.76,
        }

        mock_request.assert_called_with('GET', url, params=params)

    @mock.patch('yikyakapi.yikyak.YikYak._get_yaks')
    def test_get_new_yaks(self, mock_get):
        client = YikYak()
        client.get_new_yaks(12.34, 56.78)

        url = 'https://www.yikyak.com/api/v2/messages'
        mock_get.assert_called_with(url, 12.34, 56.78, 'new')

    @mock.patch('yikyakapi.yikyak.YikYak._get_yaks')
    def test_get_hot_yaks(self, mock_get):
        client = YikYak()
        client.get_hot_yaks(12.34, 56.78)

        url = 'https://www.yikyak.com/api/v2/messages'
        mock_get.assert_called_with(url, 12.34, 56.78, 'hot')

    @mock.patch('yikyakapi.yikyak.YikYak._get_yaks')
    def test_get_my_yaks(self, mock_get):
        client = YikYak()
        client.get_my_yaks()

        url = 'https://www.yikyak.com/api/v2/messages/myYaks'
        mock_get.assert_called_with(url)

    @mock.patch('yikyakapi.yikyak.YikYak.get_my_yaks')
    def test_get_my_new_yaks(self, mock_get):
        client = YikYak()

        with self.assertWarns(DeprecationWarning):
            client.get_my_new_yaks()

        mock_get.assert_called_with()

    def test_get_my_hot_yaks(self):
        client = YikYak()
        with self.assertRaises(NotImplementedError):
            client.get_my_hot_yaks()

    @mock.patch('yikyakapi.yikyak.YikYak._get_yaks')
    def test_get_my_replies(self, mock_get):
        client = YikYak()
        client.get_my_replies()

        url = 'https://www.yikyak.com/api/v2/messages/myReplies'
        mock_get.assert_called_with(url)

    @mock.patch('yikyakapi.yikyak.YikYak.get_my_replies')
    def test_get_my_new_replies(self, mock_get):
        client = YikYak()

        with self.assertWarns(DeprecationWarning):
            client.get_my_new_replies()

        mock_get.assert_called_with()

    def test_get_my_hot_replies(self):
        client = YikYak()
        with self.assertRaises(NotImplementedError):
            client.get_my_hot_replies()

    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test_compose_yak(self, mock_request):
        """
        Assert YikYak.compose_yak() makes the correct API call
        """
        client = YikYak()

        # Expected request
        url = "https://www.yikyak.com/api/v2/messages"
        params = {
            'lat': 50.93,
            'long': -1.76,
            'myHerd': 0,
            'userLat': 50.93,
            'userLong': -1.76,
        }
        json = {
            'handle': False,
            'message': 'Hello World',
        }

        # Anonymous
        yak = client.compose_yak("Hello World", 50.93, -1.76, False)
        self.assertTrue(isinstance(yak, Yak))
        mock_request.assert_called_with('POST', url, params=params, json=json)

        # With handle
        json['handle'] = True
        client.compose_yak("Hello World", 50.93, -1.76, True)
        mock_request.assert_called_with('POST', url, params=params, json=json)

    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test_check_handle_availability_available(self, mock_request):
        """
        check_handle_availability() must return True for an available handle
        """
        mock_request.return_value = {'code': 0}

        client = YikYak()
        result = client.check_handle_availability('available')

        url = 'https://www.yikyak.com/api/v2/yakker/handles'
        params = {
            'handle': 'available',
        }
        mock_request.assert_called_with('GET', url, params=params)
        self.assertTrue(result)

    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test_check_handle_availability_invalid(self, mock_request):
        """
        check_handle_availability() must return False for an invalid handle
        """
        mock_request.return_value = {'code': 1}

        client = YikYak()
        result = client.check_handle_availability('invalid')

        url = 'https://www.yikyak.com/api/v2/yakker/handles'
        params = {
            'handle': 'invalid',
        }
        mock_request.assert_called_with('GET', url, params=params)
        self.assertFalse(result)

    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test_check_handle_availability_unavailable(self, mock_request):
        """
        check_handle_availability() must return False for an unavailable handle
        """
        mock_request.return_value = {'code': 2}

        client = YikYak()
        result = client.check_handle_availability('unavailable')

        url = 'https://www.yikyak.com/api/v2/yakker/handles'
        params = {
            'handle': 'unavailable',
        }
        mock_request.assert_called_with('GET', url, params=params)
        self.assertFalse(result)

    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test_claim_handle(self, mock_request):
        mock_request.return_value = {'code': 0}

        client = YikYak()
        client.claim_handle('YikYakBot')
        url = 'https://www.yikyak.com/api/v2/yakker/handles'
        json = {
            'handle': 'YikYakBot',
        }
        mock_request.assert_called_with('POST', url, json=json)

    @mock.patch('yikyakapi.yikyak.Yak')
    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test_get_yak(self, mock_request, mock_yak):
        mock_request.return_value = {'mock': 'data'}
        mock_yak.return_value = mock.Mock()

        client = YikYak()
        client.session = mock.Mock()

        yak = client.get_yak('R/abcd')

        url = "https://www.yikyak.com/api/v2/messages/R%2Fabcd"
        params = {
            'userLat': 0,
            'userLong': 0,
        }

        mock_request.assert_called_with('GET', url, params=params)
        mock_yak.assert_called_with(client.session, mock_request.return_value)
        self.assertEqual(yak, mock_yak.return_value)
