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
            'nickname': "YikYakBot",
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
        self.assertEqual(comment.nickname, data['nickname'])
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
        self.assertEqual(comment.nickname, None)
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

    def test_str(self):
        comment = Comment('auth_token', {})
        comment.message = 'Hello'
        comment_str = comment.__str__()
        self.assertEqual(type(comment_str), str)
