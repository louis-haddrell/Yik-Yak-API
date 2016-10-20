import unittest
from unittest import mock

from yikyakapi.yak import *


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.yak_data = {
            'canDownVote': True,
            'canReply': True,
            'canReport': 0,
            'canUpVote': True,
            'canVote': True,
            'comments': 0,
            'deliveryID': 0,
            'gmt': 0,
            'handle': None,
            'hidePin': 0,
            'latitude': 50.93,
            'liked': 0,
            'location': {},
            'locationDisplayStyle': 0,
            'locationName': "YikYak HQ",
            'longitude': -1.76,
            'message': "Hello World!",
            'messageID': "R/abcd",
            'nickname': "YikYakBot",
            'numberOfLikes': 0,
            'posterID': "abcd",
            'readOnly': 0,
            'reyaked': 0,
            'score': 0,
            'time': "2016-10-10 10:10:10",
            'type': 0,
        }

        self.img_data = {
            'expandInFeed': 1,
            'imageHeight': 500,
            'imageWidth': 500,
            'thumbNailUrl': "http://i.imgur.com/YlplorD.png",
            'url': "http://i.imgur.com/YlplorD.png",
        }
        self.img_data.update(self.yak_data)

    def test_yak_construction(self):
        yak = Yak('auth_token', self.img_data)
        self.assertEqual(yak.base_url, "https://www.yikyak.com/api/v2/")
        self.assertEqual(yak.auth_token, 'auth_token')
        self.assertEqual(yak.can_downvote, self.img_data['canDownVote'])
        self.assertEqual(yak.can_reply, self.img_data['canReply'])
        self.assertEqual(yak.can_report, self.img_data['canReport'])
        self.assertEqual(yak.can_upvote, self.img_data['canUpVote'])
        self.assertEqual(yak.can_vote, self.img_data['canVote'])
        self.assertEqual(yak.comments, self.img_data['comments'])
        self.assertEqual(yak.delivery_id, self.img_data['deliveryID'])
        self.assertEqual(yak.expand_in_feed, self.img_data['expandInFeed'])
        self.assertEqual(yak.gmt, self.img_data['gmt'])
        self.assertEqual(yak.handle, self.img_data['handle'])
        self.assertEqual(yak.hide_pin, self.img_data['hidePin'])
        self.assertEqual(yak.image_height, self.img_data['imageHeight'])
        self.assertEqual(yak.image_width, self.img_data['imageWidth'])
        self.assertEqual(yak.latitude, self.img_data['latitude'])
        self.assertEqual(yak.liked, self.img_data['liked'])
        self.assertEqual(yak.location, self.img_data['location'])
        self.assertEqual(yak.location_display_style, self.img_data['locationDisplayStyle'])
        self.assertEqual(yak.location_name, self.img_data['locationName'])
        self.assertEqual(yak.longitude, self.img_data['longitude'])
        self.assertEqual(yak.message, self.img_data['message'])
        self.assertEqual(yak.message_id, self.img_data['messageID'])
        self.assertEqual(yak.nickname, self.img_data['nickname'])
        self.assertEqual(yak.number_of_likes, self.img_data['numberOfLikes'])
        self.assertEqual(yak.poster_id, self.img_data['posterID'])
        self.assertEqual(yak.read_only, self.img_data['readOnly'])
        self.assertEqual(yak.reyaked, self.img_data['reyaked'])
        self.assertEqual(yak.score, self.img_data['score'])
        self.assertEqual(yak.thumbnail_url, self.img_data['thumbNailUrl'])
        self.assertEqual(yak.time, self.img_data['time'])
        self.assertEqual(yak.type, self.img_data['type'])
        self.assertEqual(yak.url, self.img_data['url'])

    def test_yak_defaults(self):
        yak = Yak('auth_token', {})
        self.assertEqual(yak.base_url, "https://www.yikyak.com/api/v2/")
        self.assertEqual(yak.can_downvote, False)
        self.assertEqual(yak.can_reply, False)
        self.assertEqual(yak.can_report, 0)
        self.assertEqual(yak.can_upvote, False)
        self.assertEqual(yak.can_vote, False)
        self.assertEqual(yak.comments, 0)
        self.assertEqual(yak.comments_list, [])
        self.assertEqual(yak.delivery_id, 0)
        self.assertEqual(yak.expand_in_feed, 0)
        self.assertEqual(yak.gmt, 0)
        self.assertEqual(yak.handle, None)
        self.assertEqual(yak.hide_pin, 0)
        self.assertEqual(yak.image_height, 0)
        self.assertEqual(yak.image_width, 0)
        self.assertEqual(yak.latitude, 0.0)
        self.assertEqual(yak.liked, 0)
        self.assertEqual(yak.location, {})
        self.assertEqual(yak.location_display_style, 0)
        self.assertEqual(yak.location_name, "")
        self.assertEqual(yak.longitude, 0.0)
        self.assertEqual(yak.message, "")
        self.assertEqual(yak.message_id, "")
        self.assertEqual(yak.nickname, None)
        self.assertEqual(yak.number_of_likes, 0)
        self.assertEqual(yak.poster_id, "")
        self.assertEqual(yak.read_only, 0)
        self.assertEqual(yak.reyaked, 0)
        self.assertEqual(yak.score, 0)
        self.assertEqual(yak.thumbnail_url, None)
        self.assertEqual(yak.time, "")
        self.assertEqual(yak.type, 0)
        self.assertEqual(yak.url, None)

    def test_invalid_vote(self):
        """
        Assert that Yak._vote() throws an exception with invalid vote types

        ._vote() should only accept 'upvote' and 'downvote'
        """
        yak = Yak('auth_token', self.yak_data)

        with self.assertRaises(AssertionError):
            yak._vote('sidevote')

    def test_comments_list_constructor_default(self):
        """
        Assert a default value is provided for the comments_list if not
        included in the data passed to the constructor
        """
        yak = Yak('auth_token', {})
        self.assertEqual(yak._comments_list, [])

    @mock.patch('yikyakapi.yak.Comment')
    def test_comments_list_setter(self, mock_comment):
        yak = Yak('auth_token', {})
        yak.comments_list = range(10)
        self.assertEqual(len(yak._comments_list), 10)

    @mock.patch('yikyakapi.yak.Yak._retrieve_comments')
    def test_comments_list_getter_no_request(self, mock_retrieve):
        """
        Get the comments list without making a request
        """
        yak = Yak('auth_token', {})
        yak.comments = 3
        yak._comments_list = ['a', 'b', 'c']

        comments = yak.comments_list
        self.assertEqual(comments, ['a', 'b', 'c'])
        self.assertFalse(mock_retrieve.called)

    @mock.patch('yikyakapi.yak.Yak._request')
    def test_retrieve_comments(self, mock_request):
        """Assert ._retrieve_comments() makes the correct API call"""
        yak = Yak('auth_token', {})
        yak.message_id = 'R/abc'
        yak._retrieve_comments()

        mock_request.return_value = ['a', 'b', 'c']

        # Expected request
        url = 'https://www.yikyak.com/api/v2/messages/R%2Fabc/comments'
        params = {
            'userLat': 0,
            'userLong': 0,
        }

        comments = yak._retrieve_comments()
        mock_request.assert_called_with('GET', url, params=params)
        self.assertEqual(comments, mock_request.return_value)

    def test_str(self):
        yak = Yak('auth_token', {})
        yak.message = 'Hello'
        yak_str = yak.__str__()
        self.assertEqual(type(yak_str), str)

    @mock.patch('yikyakapi.yak.Yak._request')
    def test_compose_comment(self, mock_request):
        """
        Assert composing a comment makes the correct API call
        """
        yak = Yak('auth_token', {})
        comment = yak.compose_comment('Hello world')

        # Expected API call
        url = yak.message_url + 'comments'
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        json = {
            'handle': False,
            'comment': 'Hello world',
        }
        mock_request.assert_called_with('POST', url, params=params, json=json)

        # Check returned comment
        self.assertTrue(isinstance(comment, Comment))

    @mock.patch('yikyakapi.yak.Yak._request')
    def test_compose_comment_with_handle(self, mock_request):
        """
        Assert composing a comment makes the correct API call
        """
        yak = Yak('auth_token', {})
        comment = yak.compose_comment('Hello world', handle=True)

        # Expected API call
        url = yak.message_url + 'comments'
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        json = {
            'handle': True,
            'comment': 'Hello world',
        }
        mock_request.assert_called_with('POST', url, params=params, json=json)

        # Check returned comment
        self.assertTrue(isinstance(comment, Comment))
