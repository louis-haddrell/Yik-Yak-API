import unittest
from unittest import mock

from yikyakapi.yakker import *


class TestSuite(unittest.TestCase):
    def test_construction(self):
        session = mock.Mock()
        data = {
            'myHerd': {},
            'nickname': 'YikYakBot',
            'userID': 'ABCDEFG',
            'yakarma': 50000,
        }

        yakker = Yakker(session, data)
        self.assertEqual(yakker.base_url, 'https://www.yikyak.com/api/v2/')
        self.assertEqual(yakker.session, session)
        self.assertEqual(yakker.herd, data['myHerd'])
        self.assertEqual(yakker.nickname, data['nickname'])
        self.assertEqual(yakker.userID, data['userID'])
        self.assertEqual(yakker.yakarma, data['yakarma'])

    def test_construction_defaults(self):
        session = mock.Mock()
        yakker = Yakker(session, {})
        self.assertEqual(yakker.base_url, 'https://www.yikyak.com/api/v2/')
        self.assertEqual(yakker.session, session)
        self.assertEqual(yakker.herd, None)
        self.assertEqual(yakker.nickname, None)
        self.assertEqual(yakker.userID, None)
        self.assertEqual(yakker.yakarma, 0)

    @mock.patch('yikyakapi.yikyak.Yakker._request')
    def test_refresh(self, mock_request):
        mock_request.return_value = {}
        yakker = Yakker(mock.Mock(), {})
        yakker.refresh()

        params = {'userLat': 0, 'userLong': 0}
        url = 'https://www.yikyak.com/api/v2/yakker/init'
        mock_request.assert_called_with('GET', url, params=params)
