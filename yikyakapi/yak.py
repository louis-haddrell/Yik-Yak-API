import urllib.parse

from .comment import Comment
from .message import Message


class Yak(Message):
    def __init__(self, session, json):
        super().__init__()

        self.session = session

        self._comments_list = []
        self.can_downvote = json.get('canDownVote', False)
        self.can_reply = json.get('canReply', False)
        self.can_report = json.get('canReport', 0)
        self.can_upvote = json.get('canUpVote', False)
        self.can_vote = json.get('canVote', False)
        self.comments = json.get('comments', 0)
        self.comments_list = json.get('commentsList', [])
        self.delivery_id = json.get('deliveryID', 0)
        self.expand_in_feed = json.get('expandInFeed', 0)
        self.gmt = json.get('gmt', 0)
        self.handle = json.get('handle', None)
        self.hide_pin = json.get('hidePin', 0)
        self.image_height = json.get('imageHeight', 0)
        self.image_width = json.get('imageWidth', 0)
        self.latitude = json.get('latitude', 0.0)
        self.liked = json.get('liked', 0)
        self.location = json.get('location', {})
        self.location_display_style = json.get('locationDisplayStyle', 0)
        self.location_name = json.get('locationName', "")
        self.longitude = json.get('longitude', 0.0)
        self.message = json.get('message', "")
        self.message_id = json.get('messageID', "")
        self.nickname = json.get('nickname', None)
        self.number_of_likes = json.get('numberOfLikes', 0)
        self.poster_id = json.get('posterID', "")
        self.read_only = json.get('readOnly', 0)
        self.reyaked = json.get('reyaked', 0)
        self.score = json.get('score', 0)
        self.thumbnail_url = json.get('thumbNailUrl', None)
        self.time = json.get('time', "")
        self.type = json.get('type', 0)
        self.url = json.get('url', None)

    def __str__(self):
        return self.message.encode('ascii', 'ignore').decode()

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
        self._comments_list = [Comment(self.session, data) for data in json]

    @property
    def message_url(self):
        url = self.base_url + 'messages/{}/'
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
        return self._request('GET', url, params=self.params)

    def compose_comment(self, comment, handle=False):
        """
        Add a comment below this Yak

        Arguments:
            comment (string): the comment to post

        Returns:
            Comment object for the comment you posted
        """
        url = self.message_url + 'comments'
        json = {
            'handle': handle,
            'comment': comment,
        }
        response = self._request('POST', url, params=self.params, json=json)
        return Comment(self.session, response)

    def refresh(self):
        """
        Refresh the Yak information
        """
        url = self.message_url
        data = self._request('GET', url, params=self.params)
        self = self.__init__(self.session, data)
