import requests
import settings
import urllib.parse

from json.decoder import JSONDecodeError

from yak import Yak


class YikYak(object):
    def __init__(self):
        self.auth_token = None

    def _request(self, method, url, **kwargs):
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()

        try:
            return response.json()
        except JSONDecodeError:
            return {}

    def login(self, country_code, phone_number, pin):
        """
        Login to YikYak and get our auth token

        Arguments:
            country_code (string): country code
            phone_number (string): phone number
            user_id (string): authentication PIN from app
        """
        self.auth_token = self.pair(country_code, phone_number, pin)

    def login_id(self, country_code, phone_number, user_id):
        """
        Alternate login with YikYak user ID instead of auth PIN

        Arguments:
            country_code (string): country code
            phone_number (string): phone number
            user_id (string): YikYak user ID
        """
        pin = self.init_pairing(user_id)
        self.auth_token = self.pair(country_code, phone_number, pin)

    def init_pairing(self, user_id):
        """
        Initialise web pairing and retrieve authentication PIN

        Arguments:
            user_id (string): YikYak user ID

        Returns:
            6 digit PIN code for use with pairing
        """
        url = "https://beta.yikyak.com/api/auth/initPairing"
        data = {'userID': user_id}
        response = self._request('POST', url, data=data)
        return response['pin']

    def pair(self, country_code, phone_number, pin):
        """
        Login to YikYak to retrieve authentication token

        Arguments:
            country_code (string): 3-letter string representing country
            phone_number (string): phone number
            pin (string): authentication PIN generated by mobile app

        Returns:
            Authentication token required for further YikYak access
        """
        url = "https://beta.yikyak.com/api/auth/pair"

        headers = {
            'Referer': 'https://beta.yikyak.com/'
        }

        json = {
            'countryCode': country_code,
            'phoneNumber': phone_number,
            'pin': pin,
        }

        response = self._request('POST', url, headers=headers, json=json)
        return response

    def get_new(self, latitude, longitude):
        url = 'https://beta.yikyak.com/api/proxy/v1/messages/all/new'

        headers = {
            'Referer': 'https://beta.yikyak.com/',
            'x-access-token': self.auth_token,
        }

        params = {
            'userLat': latitude,
            'userLong': longitude,
            'lat': latitude,
            'long': longitude,
            'myHerd': 0,
        }

        response = self._request('GET', url, params=params, headers=headers)

        # Generate new Yak objects from the JSON
        yaks = [Yak(data) for data in response]
        return yaks

    def _vote(self, action, yak):
        """
        Internal function to upvote / downvote a Yak

        Arguments:
            action (string): downvote / upvote
            yak (Yak): Yak to vote on
        """
        assert action in ['downvote', 'upvote']

        # Convert / to %2F
        yak_id = urllib.parse.quote_plus(yak.messageID)

        url = 'https://beta.yikyak.com/api/proxy/v1/messages/{}/{}'
        url = url.format(yak_id, action)

        headers = {
            'Referer': 'https://beta.yikyak.com/',
            'x-access-token': self.auth_token,
        }

        params = {
            'userLat': yak.latitude,
            'userLong': yak.longitude,
            'myHerd': 0,
        }

        self._request('PUT', url, headers=headers, params=params)

    def downvote(self, yak):
        """
        Downvote a Yak

        Arguments:
            yak (Yak): Yak to downvote
        """
        self._vote('downvote', yak)

    def upvote(self, yak):
        """
        Upvote a Yak

        Arguments:
            yak (Yak): Yak to upvote
        """
        self._vote('upvote', yak)


if __name__ == "__main__":
    yakker = YikYak()
    yakker.login_id(settings.COUNTRY, settings.PHONE_NUMBER, settings.USER_ID)
    new_yaks = yakker.get_new(settings.LATITUDE, settings.LONGITUDE)

    for yak in new_yaks:
        print(yak.message.encode('ascii', 'ignore').decode())
        print()
