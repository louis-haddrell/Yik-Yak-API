# Python Yik Yak API

## Quickstart

Create a new Python module *outside* of the `yikyakapi` folder to avoid import errors e.g.

```
|- yikyakapi/
|- yakbot.py
```

### Login using PIN

Logging in to the YikYak API requires a 6 digit authentication code that can be found in the app under Settings > Authenticate for Web.

You must log in using your phone number country code, phone number and the PIN code.

```python
from yikyakapi.yikyak import YikYak

COUNTRY_CODE = "GBR"
PHONE_NUMBER = "0123456789"

if __name__ == "__main__":
    client = YikYak()
    pin = input("Web authentication PIN: ")
    client.login(COUNTRY_CODE, PHONE_NUMBER, pin)
```

### Retrieving User ID
Once you've logged in using the PIN code you can grab your user ID. **Keep this ID a secret!**

```
user_id = client.yakker.userID
print(user_id)
```

### Login using User ID

You can now use this user ID to avoid ever having to authenticate using the app.

```python
USER_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

client.login_id(COUNTRY_CODE, PHONE_NUMBER, USER_ID)
```

### Retrieve some Yaks

Retrieve Yaks from a co-ordinate:

```python
yaks = client.get_new_yaks(50.93, -1.759)
```

### Post a Yak
Post a Yak to a co-ordinate:

```python
client.compose_yak("Hello world!", 50.93, -1.759)
```
