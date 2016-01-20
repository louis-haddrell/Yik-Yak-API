
import urllib.parse

from web import WebObject


class Yak(WebObject):
    def __init__(self, auth_token, json):
        self.auth_token = auth_token

        self.can_downvote = json.get('canDownVote', False)
        self.can_reply = json.get('canReply', False)
        self.can_report = json.get('canReport', 0)
        self.can_upvote = json.get('canUpVote', False)
        self.can_vote = json.get('canVote', False)
        self.comments = json.get('comments', 0)
        self.delivery_id = json.get('deliveryID', 0)
        self.gmt = json.get('gmt', 0)
        self.handle = json.get('handle', None)
        self.hide_pin = json.get('hidePin', 0)
        self.latitude = json.get('latitude', 0.0)
        self.liked = json.get('liked', 0)
        self.location = json.get('location', {})
        self.location_display_style = json.get('locationDisplayStyle', 0)
        self.location_name = json.get('locationName', "")
        self.longitude = json.get('longitude', 0.0)
        self.message = json.get('message', "")
        self.message_id = json.get('messageID', "")
        self.number_of_likes = json.get('numberOfLikes', 0)
        self.poster_id = json.get('posterID', "")
        self.read_only = json.get('readOnly', 0)
        self.reyaked = json.get('reyaked', 0)
        self.score = json.get('score', 0)
        self.time = json.get('time', "")
        self.type = json.get('type', 0)

        # Image Yaks
        self.expand_in_feed = json.get('expandInFeed', 0)
        self.image_height = json.get('imageHeight', 0)
        self.image_width = json.get('imageWidth', 0)
        self.thumbnail_url = json.get('thumbNailUrl', None)
        self.url = json.get('url', None)

    @property
    def message_url(self):
        url = 'https://yikyak.com/api/proxy/v1/messages/{}/'
        # Convert / to %2F
        urlsafe_id = urllib.parse.quote_plus(self.message_id)
        return url.format(urlsafe_id)

    def _vote(self, action):
        """
        Internal function to upvote or downvote this Yak

        Arguments:
            action (string): downvote / upvote
        """
        assert action in ['downvote', 'upvote']

        url = self.message_url + action

        headers = {
            'Referer': 'https://yikyak.com/',
            'x-access-token': self.auth_token,
        }

        params = {
            'userLat': 0,
            'userLong': 0,
            'myHerd': 0,
        }

        self._request('PUT', url, headers=headers, params=params)

    def downvote(self):
        """Downvote this Yak"""
        self._vote('downvote')

    def upvote(self):
        """Upvote this Yak"""
        self._vote('upvote')

    def refresh(self):
        """Refresh the Yak information"""
        url = self.message_url

        headers = {
            'Referer': 'https://yikyak.com/',
            'x-access-token': self.auth_token,
        }

        params = {
            'userLat': 0,
            'userLong': 0,
            'myHerd': 0,
        }

        data = self._request('GET', url, headers=headers, params=params)
        self = self.__init__(self.auth_token, data)

    def delete(self):
        """Delete this Yak"""
        url = self.message_url

        headers = {
            'Referer': 'https://yikyak.com/',
            'x-access-token': self.auth_token,
        }
        params = {
            'userLat': 0,
            'userLong': 0,
            'myHerd': 0,
        }
        self._request('DELETE', url, headers=headers, params=params)


class Comment(object):
    def __init__(self, json):
        self.back_id = json['backID']
        self.comment = json['comment']
        self.comment_id = json['commentID']
        self.delivery_id = json['deliveryID']
        self.gmt = json['gmt']
        self.is_deleted = json['isDeleted']
        self.liked = json['liked']
        self.message_id = json['messageID']
        self.number_of_likes = json['numberOfLikes']
        self.overlay_id = json['overlayID']
        self.poster_id = json['posterID']
        self.time = json['time']
