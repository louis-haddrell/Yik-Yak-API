
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
        self._comments_list = []
        self.comments_list = json.get('commentsList', [])
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

    def __str__(self):
        return self.message.encode('ascii', 'ignore')

    # Comment Caching
    #
    # Note: Checking .comments_list *may* invoke an API request
    #
    # Yaks retrieved from the hot / new feed know their comment count, but not
    # the details of the comments themselves. These Yaks will require a request
    # to download the comments.
    #
    # Yaks that have been accessed directly, or those which have previously
    # downloaded comments, already know about their comments, so won't request.

    @property
    def comments_list(self):
        # Mismatch between number of comments and downloaded comments
        if self.comments != len(self._comments_list):
            self.comments_list = self._retrieve_comments()

        return self._comments_list

    @comments_list.setter
    def comments_list(self, json):
        self._comments_list = [Comment(self.auth_token, data) for data in json]

    @property
    def message_url(self):
        url = 'https://yikyak.com/api/proxy/v1/messages/{}/'
        # Convert / to %2F
        urlsafe_id = urllib.parse.quote_plus(self.message_id)
        return url.format(urlsafe_id)

    def _retrieve_comments(self):
        """
        Retrieve comments from this Yak

        Returns:
            JSON response from API call
        """
        url = self.message_url + 'comments'
        params = {
            'userLat': 0,
            'userLong': 0,
            'myHerd': 0,
        }
        return self._request('GET', url, params=params)

    def _vote(self, action):
        """
        Internal function to upvote or downvote this Yak

        Arguments:
            action (string): downvote / upvote
        """
        assert action in ['downvote', 'upvote']

        url = self.message_url + action
        params = {
            'userLat': 0,
            'userLong': 0,
            'myHerd': 0,
        }

        self._request('PUT', url, params=params)

    def downvote(self):
        """Downvote this Yak"""
        self._vote('downvote')

    def upvote(self):
        """Upvote this Yak"""
        self._vote('upvote')

    def refresh(self):
        """Refresh the Yak information"""
        url = self.message_url
        params = {
            'userLat': 0,
            'userLong': 0,
            'myHerd': 0,
        }

        data = self._request('GET', url, params=params)
        self = self.__init__(self.auth_token, data)

    def delete(self):
        """Delete this Yak"""
        url = self.message_url
        params = {
            'userLat': 0,
            'userLong': 0,
            'myHerd': 0,
        }

        self._request('DELETE', url, params=params)


class Comment(WebObject):
    def __init__(self, auth_token, json):
        self.auth_token = auth_token

        self.back_id = json.get('backID', '')
        self.comment = json.get('comment', '')
        self.comment_id = json.get('commentID', '')
        self.delivery_id = json.get('deliveryID', 0)
        self.gmt = json.get('gmt', 0)
        self.is_deleted = json.get('isDeleted', False)
        self.liked = json.get('liked', 0)
        self.message_id = json.get('messageID', '')
        self.number_of_likes = json.get('numberOfLikes', 0)
        self.overlay_id = json.get('overlayID', '')
        self.poster_id = json.get('posterID', '')
        self.time = json.get('time', '')


    def __str__(self):
        return self.comment.encode('ascii', 'ignore')
