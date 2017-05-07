# Python Yik Yak API

> **Note: YikYak servers are no longer active**
> YikYak has shut down so this API will no longer work

## Quickstart

### Prerequisites

The API requires Python 3 and the [requests library](http://docs.python-requests.org/en/master/), which can be installed using pip:

```bash
pip3 install requests
```

### Folder Structure
Create a new Python module *outside* of the `yikyakapi` folder to avoid import errors

```
|- yikyakapi/
|- yakbot.py
```

### Retrieving User ID

Logging in to YikYak Web requires a 6 digit authentication code. This can be found in the app under Settings > Authenticate for Web. To avoid authenticating with the app every time we want to log in, we must first retrieve our user ID. Note that this is not the same as your handle.

The following example code will print out this ID. Remember to update `COUNTRY_CODE` and `PHONE_NUMBER` to your details - a list of country codes can be found in [API documentation](api.md).

```python
from yikyakapi.yikyak import YikYak

COUNTRY_CODE = "GBR"
PHONE_NUMBER = "0123456789"

if __name__ == "__main__":
    client = YikYak()
    pin = input("Web authentication PIN: ")
    client.login_pin(COUNTRY_CODE, PHONE_NUMBER, pin)
    print(client.yakker.userID)
```

Your user ID will be displayed. This is a 32 character hex string and is not the same as your YikYak username / handle.

**It is important to keep this ID secret!**

### Authenticating with User ID

Now we can easily authenticate using our user ID instead of the PIN code:

```python
from yikyakapi.yikyak import YikYak

COUNTRY_CODE = "GBR"
PHONE_NUMBER = "0123456789"
USER_ID = '0123456789ABCDEF0123456789ABCDEF'

if __name__ == "__main__":
    client = YikYak()
    pin = input("Web authentication PIN: ")
    client.login_id(COUNTRY_CODE, PHONE_NUMBER, USER_ID)
```

## The Basics

### Retrieving Yaks

Retrieve Yaks from a co-ordinate:

```python
yaks = client.get_new_yaks(50.93, -1.759)
```

### Post a Yak
Post a Yak to a co-ordinate anonymously:

```python
client.compose_yak("Hello world!", 50.93, -1.759, False)
```

Post a Yak to a co-ordinate with your handle enabled:

```python
client.compose_yak("Hello world!", 50.93, -1.759, True)
```
