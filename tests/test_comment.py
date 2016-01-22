import unittest

from unittest import mock
from yak import Comment


class TestSuite(unittest.TestCase):
    def test_constructor(self):
        data = {
            'backID': '001',
            'comment': 'Hello World',
            'commentID': 'R/1234',
            'deliveryID': 0,
            'gmt': 0,
            'isDeleted': False,
            'liked': 0,
            'messageID': 'R/abcd',
            'numberOfLikes': 0,
            'overlayID': '001',
            'posterID': 'poster',
            'time': '2016-01-01 10:00:00',
        }

        comment = Comment('auth_token', data)

        self.assertEqual(comment.auth_token, 'auth_token')

        self.assertEqual(comment.back_id, data['backID'])
        self.assertEqual(comment.comment, data['comment'])
        self.assertEqual(comment.comment_id, data['commentID'])
        self.assertEqual(comment.delivery_id, data['deliveryID'])
        self.assertEqual(comment.gmt, data['gmt'])
        self.assertEqual(comment.is_deleted, data['isDeleted'])
        self.assertEqual(comment.liked, data['liked'])
        self.assertEqual(comment.message_id, data['messageID'])
        self.assertEqual(comment.number_of_likes, data['numberOfLikes'])
        self.assertEqual(comment.overlay_id, data['overlayID'])
        self.assertEqual(comment.poster_id, data['posterID'])
        self.assertEqual(comment.time, data['time'])

    def test_constructor_defaults(self):
        """Assert Comment can be constructed with missing data"""
        comment = Comment('auth_token', {})

        self.assertEqual(comment.auth_token, 'auth_token')

        self.assertEqual(comment.back_id, '')
        self.assertEqual(comment.comment, '')
        self.assertEqual(comment.comment_id, '')
        self.assertEqual(comment.delivery_id, 0)
        self.assertEqual(comment.gmt, 0)
        self.assertEqual(comment.is_deleted, False)
        self.assertEqual(comment.liked, 0)
        self.assertEqual(comment.message_id, '')
        self.assertEqual(comment.number_of_likes, 0)
        self.assertEqual(comment.overlay_id, '')
        self.assertEqual(comment.poster_id, '')
        self.assertEqual(comment.time, '')

    def test_message_url(self):
        """Assert Comment correctly generates its URL"""
        comment = Comment('auth_token', {})
        comment.message_id = 'R/1234'
        comment.comment_id = 'R/abcd'
        expected = 'https://yikyak.com/api/proxy/v1/messages/R%2F1234/comments/R%2Fabcd/'
        self.assertEqual(comment.message_url, expected)

    @mock.patch('yak.Comment._request')
    def test_upvote(self, mock_request):
        """Assert the upvote API call is made correctly for this Comment"""
        comment = Comment('auth_token', {})
        comment.comment_id = 'R/abcd'
        comment.message_id = 'R/1234'
        comment.upvote()

        # Assert API call is correct
        url = comment.message_url + 'upvote'
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        mock_request.assert_called_with('PUT', url, params=params)

    @mock.patch('yak.Comment._request')
    def test_downvote(self, mock_request):
        """Assert the downvote API call is made correctly for this Comment"""
        comment = Comment('auth_token', {})
        comment.comment_id = 'R/abcd'
        comment.message_id = 'R/1234'
        comment.downvote()

        # Assert API call is correct
        url = comment.message_url + 'downvote'
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        mock_request.assert_called_with('PUT', url, params=params)

    @mock.patch('yak.Comment._request')
    def test_delete(self, mock_request):
        """
        Assert that Comment.delete() makes the correct API call
        """
        comment = Comment('auth_token', {})
        comment.comment_id = 'R/abcd'
        comment.message_id = 'R/1234'
        comment.delete()

        # Expected request
        url = comment.message_url
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        mock_request.assert_called_with('DELETE', url, params=params)

    def test_str(self):
        comment = Comment('auth_token', {})
        comment.message = 'Hello'
        comment_str = comment.__str__()
        self.assertEqual(type(comment_str), str)
