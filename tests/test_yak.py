import unittest
from unittest import mock

from yak import *


class YakTests(unittest.TestCase):
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
        yak = Yak('auth_token', self.yak_data)

        self.assertEqual(yak.auth_token, 'auth_token')

        # Check retrieval of JSON data
        self.assertEqual(yak.can_downvote, self.yak_data['canDownVote'])
        self.assertEqual(yak.can_reply, self.yak_data['canReply'])
        self.assertEqual(yak.can_report, self.yak_data['canReport'])
        self.assertEqual(yak.can_upvote, self.yak_data['canUpVote'])
        self.assertEqual(yak.can_vote, self.yak_data['canVote'])
        self.assertEqual(yak.comments, self.yak_data['comments'])
        self.assertEqual(yak.delivery_id, self.yak_data['deliveryID'])
        self.assertEqual(yak.gmt, self.yak_data['gmt'])
        self.assertEqual(yak.handle, self.yak_data['handle'])
        self.assertEqual(yak.hide_pin, self.yak_data['hidePin'])
        self.assertEqual(yak.latitude, self.yak_data['latitude'])
        self.assertEqual(yak.liked, self.yak_data['liked'])
        self.assertEqual(yak.location, self.yak_data['location'])
        self.assertEqual(
            yak.location_display_style,
            self.yak_data['locationDisplayStyle']
        )
        self.assertEqual(yak.location_name, self.yak_data['locationName'])
        self.assertEqual(yak.longitude, self.yak_data['longitude'])
        self.assertEqual(yak.message, self.yak_data['message'])
        self.assertEqual(yak.message_id, self.yak_data['messageID'])
        self.assertEqual(yak.number_of_likes, self.yak_data['numberOfLikes'])
        self.assertEqual(yak.poster_id, self.yak_data['posterID'])
        self.assertEqual(yak.read_only, self.yak_data['readOnly'])
        self.assertEqual(yak.reyaked, self.yak_data['reyaked'])
        self.assertEqual(yak.score, self.yak_data['score'])
        self.assertEqual(yak.time, self.yak_data['time'])
        self.assertEqual(yak.type, self.yak_data['type'])

        # Check non-image defaults
        self.assertEqual(yak.expand_in_feed, 0)
        self.assertEqual(yak.image_height, 0)
        self.assertEqual(yak.image_width, 0)
        self.assertEqual(yak.thumbnail_url, None)
        self.assertEqual(yak.url, None)

    def test_image_yak_construction(self):
        yak = Yak('auth_token', self.img_data)

        self.assertEqual(yak.can_downvote, self.img_data['canDownVote'])
        self.assertEqual(yak.can_reply, self.img_data['canReply'])
        self.assertEqual(yak.can_report, self.img_data['canReport'])
        self.assertEqual(yak.can_upvote, self.img_data['canUpVote'])
        self.assertEqual(yak.can_vote, self.img_data['canVote'])
        self.assertEqual(yak.comments, self.img_data['comments'])
        self.assertEqual(yak.delivery_id, self.img_data['deliveryID'])
        self.assertEqual(yak.gmt, self.img_data['gmt'])
        self.assertEqual(yak.handle, self.img_data['handle'])
        self.assertEqual(yak.hide_pin, self.img_data['hidePin'])
        self.assertEqual(yak.latitude, self.img_data['latitude'])
        self.assertEqual(yak.liked, self.img_data['liked'])
        self.assertEqual(yak.location, self.img_data['location'])
        self.assertEqual(
            yak.location_display_style,
            self.img_data['locationDisplayStyle']
        )
        self.assertEqual(yak.location_name, self.img_data['locationName'])
        self.assertEqual(yak.longitude, self.img_data['longitude'])
        self.assertEqual(yak.message, self.img_data['message'])
        self.assertEqual(yak.message_id, self.img_data['messageID'])
        self.assertEqual(yak.number_of_likes, self.img_data['numberOfLikes'])
        self.assertEqual(yak.poster_id, self.img_data['posterID'])
        self.assertEqual(yak.read_only, self.img_data['readOnly'])
        self.assertEqual(yak.reyaked, self.img_data['reyaked'])
        self.assertEqual(yak.score, self.img_data['score'])
        self.assertEqual(yak.time, self.img_data['time'])
        self.assertEqual(yak.type, self.img_data['type'])
        self.assertEqual(yak.expand_in_feed, self.img_data['expandInFeed'])
        self.assertEqual(yak.image_height, self.img_data['imageHeight'])
        self.assertEqual(yak.image_width, self.img_data['imageWidth'])
        self.assertEqual(yak.thumbnail_url, self.img_data['thumbNailUrl'])
        self.assertEqual(yak.url, self.img_data['url'])

    @mock.patch('yak.Yak._request')
    def test_upvote(self, mock_request):
        yak = Yak('auth_token', self.yak_data)
        yak.upvote()

        # Assert API call is correct
        url = 'https://yikyak.com/api/proxy/v1/messages/R%2Fabcd/upvote'
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        mock_request.assert_called_with('PUT', url, params=params)

    @mock.patch('yak.Yak._request')
    def test_downvote(self, mock_request):
        yak = Yak('auth_token', self.yak_data)
        yak.downvote()

        # Assert API call is correct
        url = 'https://yikyak.com/api/proxy/v1/messages/R%2Fabcd/downvote'

        params = {
            'userLat': 0,
            'userLong': 0,
        }

        mock_request.assert_called_with('PUT', url, params=params)

    def test_invalid_vote(self):
        """
        Assert that Yak._vote() throws an exception with invalid vote types

        ._vote() should only accept 'upvote' and 'downvote'
        """
        yak = Yak('auth_token', self.yak_data)

        with self.assertRaises(AssertionError):
            yak._vote('sidevote')

    @mock.patch('yak.Yak._request')
    def test_delete(self, mock_request):
        """
        Assert that Yak.delete() makes the correct API call
        """
        yak = Yak('auth_token', self.yak_data)
        yak.delete()

        # Expected request
        url = 'https://yikyak.com/api/proxy/v1/messages/R%2Fabcd/'
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        mock_request.assert_called_with('DELETE', url, params=params)

    def test_comments_list_constructor_default(self):
        """
        Assert a default value is provided for the comments_list if not
        included in the data passed to the constructor
        """
        yak = Yak('auth_token', {})
        self.assertEqual(yak._comments_list, [])

    @mock.patch('yak.Comment')
    def test_comments_list_setter(self, mock_comment):
        yak = Yak('auth_token', {})
        yak.comments_list = range(10)
        self.assertEqual(len(yak._comments_list), 10)

    @mock.patch('yak.Yak._retrieve_comments')
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

    @mock.patch('yak.Yak._request')
    def test_retrieve_comments(self, mock_request):
        """Assert ._retrieve_comments() makes the correct API call"""
        yak = Yak('auth_token', {})
        yak.message_id = 'R/abc'
        yak._retrieve_comments()

        mock_request.return_value = ['a', 'b', 'c']

        # Expected request
        url = 'https://yikyak.com/api/proxy/v1/messages/R%2Fabc/comments'
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

    # @mock.patch('yak.Yak._retrieve_comments')
    # def test_comments_list_getter_no_request(self, mock_retrieve):
    #     """
    #     Get the comments list when a request is required
    #     """
    #     yak = Yak('auth_token', {})
    #     yak.comments = 3
    #     yak._comments_list = []

    #     mock_retrieve.return_value = ['a', 'b', 'c']

    #     comments = yak.comments_list
    #     self.assertEqual(comments, ['a', 'b', 'c'])
    #     self.assertTrue(mock_retrieve.called)


class CommentTests(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
