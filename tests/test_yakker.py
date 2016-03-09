import unittest
from unittest import mock

from yakker import *


class TestSuite(unittest.TestCase):
    @mock.patch('yikyak.Yakker._request')
    def test_construction(self, mock_request):
        data = {
            'myHerd': {},
            'nickname': 'YikYakBot',
            'userID': 'ABCDEFG',
            'yakarma': 50000,
        }

        yakker = Yakker('auth_token', data)
        self.assertEqual(yakker.auth_token, 'auth_token')
        self.assertEqual(yakker.herd, data['myHerd'])
        self.assertEqual(yakker.nickname, data['nickname'])
        self.assertEqual(yakker.userID, data['userID'])
        self.assertEqual(yakker.yakarma, data['yakarma'])

    @mock.patch('yikyak.Yakker._request')
    def test_construction_defaults(self, mock_request):
        yakker = Yakker('auth_token', {})
        self.assertEqual(yakker.herd, None)
        self.assertEqual(yakker.nickname, None)
        self.assertEqual(yakker.userID, None)
        self.assertEqual(yakker.yakarma, 0)
