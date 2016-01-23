import unittest

from unittest import mock
from yak import Message


class TestSuite(unittest.TestCase):
    def test_message_url(self):
        message = Message()

        with self.assertRaises(NotImplementedError):
            message.message_url

    def test_vote_invalid(self):
        message = Message()

        with self.assertRaises(AssertionError):
            message._vote('qwerty')

    @mock.patch('yak.Message._request')
    @mock.patch('yak.Message.message_url')
    def test_vote_upvote(self, mock_url, mock_request):
        mock_url.__get__ = mock.Mock(return_value='https://www.yikyak.com/')

        message = Message()
        message._vote('upvote')

        # Expected API call
        method = 'PUT'
        url = 'https://www.yikyak.com/upvote'
        params = {
            'userLat': 0,
            'userLong': 0,
        }

        mock_request.assert_called_with(method, url, params=params)

    @mock.patch('yak.Message._request')
    @mock.patch('yak.Message.message_url')
    def test_vote_downvote(self, mock_url, mock_request):
        mock_url.__get__ = mock.Mock(return_value='https://www.yikyak.com/')

        message = Message()
        message._vote('downvote')

        # Expected API call
        method = 'PUT'
        url = 'https://www.yikyak.com/downvote'
        params = {
            'userLat': 0,
            'userLong': 0,
        }

        mock_request.assert_called_with(method, url, params=params)

    @mock.patch('yak.Message._vote')
    def test_downvote(self, mock_vote):
        message = Message()
        message.downvote()
        mock_vote.assert_called_with('downvote')

    @mock.patch('yak.Message._vote')
    def test_upvote(self, mock_vote):
        message = Message()
        message.upvote()
        mock_vote.assert_called_with('upvote')

    @mock.patch('yak.Message._request')
    @mock.patch('yak.Message.message_url')
    def test_delete(self, mock_url, mock_request):
        mock_url.__get__ = mock.Mock(return_value='https://www.yikyak.com/')

        message = Message()
        message.delete()

        # Expected API call
        method = 'DELETE'
        url = 'https://www.yikyak.com/'
        params = {
            'userLat': 0,
            'userLong': 0,
        }

        mock_request.assert_called_with(method, url, params=params)

    @mock.patch('yak.Message._request')
    @mock.patch('yak.Message.message_url')
    def test_report_other(self, mock_url, mock_request):
        """
        Assert reporting for 'Other' makes the correct API call
        """
        mock_url.__get__ = mock.Mock(return_value='https://www.yikyak.com/')

        message = Message()
        message.report(0, block=False)

        # Expected API call
        method = 'PUT'
        url = 'https://www.yikyak.com/report'
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        json = {
            'block': False,
            'reason': 'Other',
        }

        mock_request.assert_called_with(method, url, params=params, json=json)

    @mock.patch('yak.Message._request')
    @mock.patch('yak.Message.message_url')
    def test_report_offensive(self, mock_url, mock_request):
        """
        Assert reporting for 'Offensive Content' makes the correct API call
        """
        mock_url.__get__ = mock.Mock(return_value='https://www.yikyak.com/')

        message = Message()
        message.report(1, block=False)

        # Expected API call
        method = 'PUT'
        url = 'https://www.yikyak.com/report'
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        json = {
            'block': False,
            'reason': 'Offensive',
        }

        mock_request.assert_called_with(method, url, params=params, json=json)

    @mock.patch('yak.Message._request')
    @mock.patch('yak.Message.message_url')
    def test_report_spam(self, mock_url, mock_request):
        """
        Assert reporting for 'Spam' makes the correct API call
        """
        mock_url.__get__ = mock.Mock(return_value='https://www.yikyak.com/')

        message = Message()
        message.report(2, block=False)

        # Expected API call
        method = 'PUT'
        url = 'https://www.yikyak.com/report'
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        json = {
            'block': False,
            'reason': 'Spam',
        }

        mock_request.assert_called_with(method, url, params=params, json=json)

    @mock.patch('yak.Message._request')
    @mock.patch('yak.Message.message_url')
    def test_report_targeting(self, mock_url, mock_request):
        """
        Assert reporting for 'post targets someone' makes the correct API call
        """
        mock_url.__get__ = mock.Mock(return_value='https://www.yikyak.com/')

        message = Message()
        message.report(3, block=False)

        # Expected API call
        method = 'PUT'
        url = 'https://www.yikyak.com/report'
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        json = {
            'block': False,
            'reason': 'Targeting',
        }

        mock_request.assert_called_with(method, url, params=params, json=json)
