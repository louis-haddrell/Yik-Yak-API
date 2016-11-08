from .web import WebObject


class Yakker(WebObject):
    def __init__(self, session, data):
        super().__init__()

        self.session = session

        self.herd = data.get('myHerd', None)
        self.nickname = data.get('nickname', None)
        self.personaID = data.get('personaID', None)
        self.userID = data.get('userID', None)
        self.yakarma = data.get('yakarma', 0)

    def refresh(self):
        url = self.base_url + 'yakker/init'
        params = {
            'userLat': 0,
            'userLong': 0,
        }
        json = self._request('GET', url, params=params)
        data = json.get('yakker', {})
        self.__init__(self.session, data)
