import requests
import settings

ENDPOINT = "https://beta.yikyak.com/api/proxy/v1/"


def pair(country, phone, auth):
    """
    Pair your phone with the web app

    Arguments:
        country (string): country code
        phone (string): phone number
        auth (string): 6-digit authentication code
    """
    url = "https://beta.yikyak.com/api/auth/pair"

    headers = {
        'Referer': 'https://beta.yikyak.com/',
    }

    payload = {
        'countryCode': country,
        'phoneNumber': phone,
        'pin': auth,
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


if __name__ == "__main__":
    pair_response = pair("GBR", settings.PHONE_NUMBER, "258928")
    print(pair_response)
