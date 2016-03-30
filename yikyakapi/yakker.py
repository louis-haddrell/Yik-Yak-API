from .web import WebObject


class Yakker(WebObject):
    def __init__(self, auth_token, data):
        self.auth_token = auth_token
        self.herd = data.get('myHerd', None)
        self.nickname = data.get('nickname', None)
        self.userID = data.get('userID', None)
        self.yakarma = data.get('yakarma', 0)

    def refresh(self):
        url = 'https://www.yikyak.com/api/proxy/v1/yakker'
        data = self._request('GET', url)
        self.__init__(self.auth_token, data)
