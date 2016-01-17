
import unittest
from unittest import mock

from yikyak import *


class TestSuite(unittest.TestCase):
    @mock.patch('yikyak.requests')
    def test_login(self, mock_request):
        """
        Assert _login() makes correct API call
        """
        yakker = YikYak("", "", "")

        # Mock response
        mock_resp = mock.Mock()
        mock_resp.json.return_value = "authtoken"
        mock_request.post.return_value = mock_resp

        # Expected values
        url = "https://beta.yikyak.com/api/auth/pair"
        headers = {'Referer': 'https://beta.yikyak.com/'}
        json = {
            'countryCode': "GBR",
            'phoneNumber': "0000000000",
            'pin': "123456",
        }

        token = yakker._login("GBR", "0000000000", "123456")
        self.assertEqual(token, "authtoken")
        mock_request.post.assert_called_with(url, headers=headers, json=json)


if __name__ == "__main__":
    unittest.main()
