from .web import WebObject


class Message(WebObject):
    """
    Base class for Yaks and Comments

    Provides shared functionality for message-like objects including applying
    votes, deleting and reporting.
    """

    def __init__(self):
        self.params = {
            'userLat': 0,
            'userLong': 0,
        }

    @property
    def message_url(self):
        """Make sure to implement this in subclasses"""
        raise NotImplementedError

    def _vote(self, action):
        """
        Internal function to upvote or downvote the message

        Arguments:
            action (string): downvote / upvote
        """
        assert action in ['downvote', 'upvote']

        url = self.message_url + action
        self._request('PUT', url, params=self.params)

    def downvote(self):
        """Apply a downvote"""
        self._vote('downvote')

    def upvote(self):
        """Apply an upvote"""
        self._vote('upvote')

    def delete(self):
        """Delete this Message"""
        url = self.message_url
        self._request('DELETE', url, params=self.params)

    def report(self, reason, block=False):
        reasons = ["Other", "Offensive", "Spam", "Targeting"]

        url = self.message_url + "report"
        json = {
            'block': block,
            'reason': reasons[reason],
        }
        self._request('PUT', url, params=self.params, json=json)
