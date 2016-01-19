import unittest
from unittest import mock

from yak import *


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
            'messageID': "R/abcdef0123456789abcdef0123456",
            'numberOfLikes': 0,
            'posterID': "abcdef0123456789abcdef0123456",
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
        self.assertEqual(yak.location_display_style, self.yak_data['locationDisplayStyle'])
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
        self.assertEqual(yak.location_display_style, self.img_data['locationDisplayStyle'])
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
        url = 'https://beta.yikyak.com/api/proxy/v1/messages/R%2Fabcdef0123456789abcdef0123456/upvote'

        headers = {
            'Referer': 'https://beta.yikyak.com/',
            'x-access-token': 'auth_token',
        }

        params = {
            'userLat': 50.93,
            'userLong': -1.76,
            'myHerd': 0,
        }

        mock_request.assert_called_with('PUT', url, headers=headers, params=params)

    @mock.patch('yak.Yak._request')
    def test_downvote(self, mock_request):
        yak = Yak('auth_token', self.yak_data)
        yak.downvote()

        # Assert API call is correct
        url = 'https://beta.yikyak.com/api/proxy/v1/messages/R%2Fabcdef0123456789abcdef0123456/downvote'

        headers = {
            'Referer': 'https://beta.yikyak.com/',
            'x-access-token': 'auth_token',
        }

        params = {
            'userLat': 50.93,
            'userLong': -1.76,
            'myHerd': 0,
        }

        mock_request.assert_called_with('PUT', url, headers=headers, params=params)

    def test_invalid_vote(self):
        """
        Assert that Yak._vote() throws an exception with invalid vote types

        ._vote() should only accept 'upvote' and 'downvote'
        """
        yak = Yak('auth_token', self.yak_data)

        with self.assertRaises(AssertionError):
            yak._vote('sidevote')


if __name__ == '__main__':
    unittest.main()
