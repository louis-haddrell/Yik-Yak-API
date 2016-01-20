import settings

from web import WebObject
from yak import Yak


class YikYak(WebObject):
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
        url = "https://yikyak.com/api/auth/initPairing"
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
        url = "https://yikyak.com/api/auth/pair"

        json = {
            'countryCode': country_code,
            'phoneNumber': phone_number,
            'pin': pin,
        }

        response = self._request('POST', url, json=json)
        return response

    def _get_yaks(self, feed, latitude, longitude):
        """
        Internal function to retrieve Yaks from a location

        Arguments:
            feed (string): hot or new
            latitude (float): latitude co-ordinate
            longitude (float): longitude co-ordinate

        Returns:
            List of Yak objects from the feed
        """
        assert feed in ['hot', 'new']

        url = 'https://yikyak.com/api/proxy/v1/messages/all/' + feed

        params = {
            'userLat': latitude,
            'userLong': longitude,
            'lat': latitude,
            'long': longitude,
            'myHerd': 0,
        }

        response = self._request('GET', url, params=params, headers=headers)

        # Generate new Yak objects from the JSON
        yaks = [Yak(self.auth_token, data) for data in response]
        return yaks

    def get_new(self, latitude, longitude):
        """
        Retrieve new Yaks from a location

        Arguments:
            latitude (float): location latitude
            longitude (float): location longitude

        Returns:
            List of Yak objects
        """
        return self._get_yaks('new', latitude, longitude)

    def get_hot(self, latitude, longitude):
        """
        Retrieve hot Yaks from a location

        Arguments:
            latitude (float): location latitude
            longitude (float): location longitude

        Returns:
            List of Yak objects
        """
        return self._get_yaks('hot', latitude, longitude)

    def compose_yak(self, message, latitude, longitude):
        """
        Compose a new Yak at a co-ordinate

        Arguments:
            message (string): contents of Yak
            latitude (float): location latitude
            longitude (float): location longitude
        """
        url = "https://yikyak.com/api/proxy/v1/messages"
        params = {
            'lat': latitude,
            'long': longitude,
            'myHerd': 0,
            'userLat': 0,
            'userLong': 0,
        }
        json = {
            'message': message,
        }

        data = self._request('POST', url, params=params, json=json)
        return Yak(self.auth_token, data)
