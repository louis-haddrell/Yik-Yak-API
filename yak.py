
import urllib.parse

from web import WebObject


class Yak(WebObject):
    def __init__(self, auth_token, json):
        self.auth_token = auth_token

        self.can_downvote = json['canDownVote']
        self.can_reply = json['canReply']
        self.can_report = json['canReport']
        self.can_upvote = json['canUpVote']
        self.can_vote = json['canVote']
        self.comments = json['comments']
        self.delivery_id = json['deliveryID']
        self.gmt = json['gmt']
        self.handle = json['handle']
        self.hide_pin = json['hidePin']
        self.latitude = json['latitude']
        self.liked = json['liked']
        self.location = json['location']
        self.location_display_style = json['locationDisplayStyle']
        self.location_name = json['locationName']
        self.longitude = json['longitude']
        self.message = json['message']
        self.message_id = json['messageID']
        self.number_of_likes = json['numberOfLikes']
        self.poster_id = json['posterID']
        self.read_only = json['readOnly']
        self.reyaked = json['reyaked']
        self.score = json['score']
        self.time = json['time']
        self.type = json['type']

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
