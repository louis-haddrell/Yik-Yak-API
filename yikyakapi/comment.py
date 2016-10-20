import urllib.parse

from .message import Message


class Comment(Message):
    def __init__(self, auth_token, json):
        super().__init__()

        self.auth_token = auth_token

        self.back_id = json.get('backID', '')
        self.comment = json.get('comment', '')
        self.comment_id = json.get('commentID', '')
        self.delivery_id = json.get('deliveryID', 0)
        self.gmt = json.get('gmt', 0)
        self.is_deleted = json.get('isDeleted', False)
        self.liked = json.get('liked', 0)
        self.message_id = json.get('messageID', '')
        self.nickname = json.get('nickname', None)
        self.number_of_likes = json.get('numberOfLikes', 0)
        self.overlay_id = json.get('overlayID', '')
        self.poster_id = json.get('posterID', '')
        self.time = json.get('time', '')

    @property
    def message_url(self):
        url = self.base_url + 'messages/{}/comments/{}/'
        # Convert / to %2F
        message_id = urllib.parse.quote_plus(self.message_id)
        comment_id = urllib.parse.quote_plus(self.comment_id)
        return url.format(message_id, comment_id)

    def __str__(self):
        return self.comment.encode('ascii', 'ignore').decode()
