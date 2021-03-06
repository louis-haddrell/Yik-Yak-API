import json
import unittest
import warnings

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
        client.yakker = mock.Mock()

        client.pair("GBR", "1234567890", "123456")

        self.assertEqual(client.yakker, None)

    def test_login(self):
        """Test deprecation of .login()"""
        client = YikYak()
        client.login_pin = mock.Mock()

        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter("always")

            client.login("GBR", "1234567890", "123456")
            client.login_pin.assert_called_with("GBR", "1234567890", "123456")

            self.assertEqual(1, len(warns))
            self.assertEqual(DeprecationWarning, warns[-1].category)
            self.assertEqual(
                "YikYak.login() is deprecated. Please use YikYak.login_pin()",
                str(warns[-1].message)
            )

    @mock.patch('yikyakapi.yikyak.Yakker')
    def test_login_pin(self, mock_yakker):
        """Assert .login_pin() retrieves the access token and CSRF token"""
        client = YikYak()
        client.pair = mock.Mock()
        client.pair.return_value = "ACCESSTOKEN"
        client.get_csrf_token = mock.Mock()
        client.get_csrf_token.return_value = "CSRFTOKEN"

        client.login_pin("GBR", "1234567890", "123456")

        client.pair.assert_called_with("GBR", "1234567890", "123456")
        client.get_csrf_token.assert_called_with()

        self.assertIn('x-access-token', client.session.headers)
        self.assertEqual("ACCESSTOKEN", client.session.headers['x-access-token'])

        self.assertIn('X-Csrf-Token', client.session.headers)
        self.assertEqual("CSRFTOKEN", client.session.headers['X-Csrf-Token'])        

        # Ensure the Yakker object has been initialised correctly
        self.assertNotEqual(None, client.yakker)
        client.yakker.refresh.assert_called_with()


    @mock.patch('yikyakapi.yikyak.Yakker')
    def test_login_pin_whitespace(self, mock_yakker):
        """Ensure whitespace is stripped from the PIN"""
        client = YikYak()
        client.pair = mock.Mock()
        client.get_csrf_token = mock.Mock()

        client.login_pin("GBR", "1234567890", " 1 2 3 4 5 6 ")

        client.pair.assert_called_with("GBR", "1234567890", "123456")

    @mock.patch('yikyakapi.yikyak.Yakker.refresh')
    @mock.patch('yikyakapi.yikyak.YikYak.get_csrf_token')
    @mock.patch('yikyakapi.yikyak.YikYak.pair')
    def test_login_pin_bad_pin(self, mock_pair, mock_csrf, mock_yakker):
        """Raise warning if the PIN code looks invalid"""
        client = YikYak()
        client.session = mock.Mock()

        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter("always")
            client.login_pin("GBR", "1234567890", "ABCDEFGH")
            self.assertEqual(1, len(warns))
            self.assertIn("PIN may be invalid", str(warns[0].message))

    @mock.patch('yikyakapi.yikyak.Yakker.refresh')
    @mock.patch('yikyakapi.yikyak.YikYak.get_csrf_token')
    @mock.patch('yikyakapi.yikyak.YikYak.pair')
    def test_login_pin_bad_pin_2(self, mock_pair, mock_csrf, mock_yakker):
        """Raise warning if the PIN code looks invalid"""
        client = YikYak()
        client.session = mock.Mock()

        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter("always")
            client.login_pin("GBR", "1234567890", "1234567")
            self.assertEqual(1, len(warns))
            self.assertIn("PIN may be invalid", str(warns[0].message))

    def test_login_id(self):
        """Test the process of logging in with the user ID"""
        client = YikYak()
        client.login_pin = mock.Mock()
        client.init_pairing = mock.Mock()
        client.init_pairing.return_value = "123456"

        client.login_id("GBR", "1234567890", "ABCDEFG")

        client.init_pairing.assert_called_with("ABCDEFG")
        client.login_pin.assert_called_with("GBR", "1234567890", "123456")

    def test_login_id_pin(self):
        """Raise warning if the UserId looks like a PIN code"""
        client = YikYak()
        client.login_pin = mock.Mock()
        client.init_pairing = mock.Mock()

        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter("always")
            client.login_id("GBR", "1234567890", "123456")
            self.assertEqual(1, len(warns))
            self.assertIn("PIN", str(warns[0].message)) 

    def test_get_csrf_token(self):
        client = YikYak()

        html = "\"csrfToken\":\"ekyJ0Oht-HaDXAMs6fd_H1Qz-E7GZvNkAzS0\""
        response = mock.Mock()
        response.text = html

        client.session = mock.Mock()
        client.session.get.return_value = response

        token = client.get_csrf_token()
        self.assertEqual(token, 'ekyJ0Oht-HaDXAMs6fd_H1Qz-E7GZvNkAzS0')

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

    @mock.patch('yikyakapi.yikyak.YikYak._upload_image')
    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test_compose_yak_image(self, mock_request, mock_upload):
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
            'imageId': mock_upload.return_value,
        }

        image = mock.Mock()
        client.compose_yak("Hello World", 50.93, -1.76, False, image)
        mock_request.assert_called_with('POST', url, params=params, json=json)

    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test__get_aws_url(self, mock_request):
        client = YikYak()
        client._get_aws_url()

        url = "https://www.yikyak.com/api/v2/photo/getUrl"
        mock_request.assert_called_with('GET', url)

    @mock.patch('yikyakapi.yikyak.YikYak._get_aws_url')
    @mock.patch('yikyakapi.yikyak.YikYak._request')
    def test__upload_image(self, mock_request, mock_aws):
        mock_aws.return_value = {
            'url': "test.com",
            'imageId': "abc123",
        }

        client = YikYak()

        image = mock.Mock()
        image_id = client._upload_image(image)

        self.assertEqual(image_id, "abc123")

        mock_aws.assert_called_with()
        mock_request.assert_called_with('PUT', "test.com", data=image.read.return_value)
