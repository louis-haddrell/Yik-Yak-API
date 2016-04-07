#YikYak Web API

##Rate Limiting
The API is rate limited to 30 requests per 60 seconds. Breaching this limit will cause the server to return an `HTTP 429` code, so take it slow.

##JSON Objects

###Yak

|Key|Value Type|Description
|---|---|---
|`canDownVote`|bool
|`canReply`|bool|
|`canReport`|int|`0` or `1`
|`canUpVote`|bool
|`canVote`|bool
|`comments`|int|Number of comments
|`deliveryID`|int|Inverse position in list (i.e. 0 at bottom)
|`gmt`|float
|`handle`|null|Unused
|`hidePin`|int|`0` or `1`
|`latitude`|float|Yak latitude to 2dp
|`liked`|int|`0` or `1`
|`location`|dict|Appears to be always empty
|`locationDisplayStyle`|int|Always `0`
|`locationName`|string
|`longitude`|float|Yak long to 2 decimal places
|`message`|string|Yak contents
|`messageID`|string|ID of Yak
|`nickname`|string|Yak author's handle
|`numberOfLikes`|int|Current Yak score
|`posterID`|string|
|`readOnly`|int|`0` or `1`
|`reyaked`|int|`0` or `1`
|`score`|float
|`time`|timestamp|`YYYY-MM-DD HH:MM:SS`
|`type`|int|`0` = text; `6` = image
|**Image Yaks Only**
|`expandInFeed`|int|Always `1`
|`imageHeight`|int|Pixel height
|`imageWidth`|int|Pixel width
|`thumbNailUrl`|url|Link to thumb
|`url`|url|Link to full size image

###Comment
|Key|Value|Notes
|---|---|---
|`backID`|string|Icon background
|`comment`|string|Comment body
|`commentID`|string
|`deliveryID`|int
|`gmt`|float
|`isDeleted`|bool
|`liked`|int|`0` or `1`
|`messageID`|string|ID of parent Yak
|`nickname`|string|Comment author's handle
|`numberOfLikes`|int
|`overlayID`|string|Icon
|`posterID`|string
|`time`|timestamp|`YYYY-MM-DD HH:MM:SS`

##Authenticating

###Pairing
`POST https://www.yikyak.com/api/auth/pair`  

To perform any further actions with the Web Beta API, we need an authentication token which can be retrieved using our country code, phone number and YikYak auth PIN (either from the mobile app, or retrieved from `initPairing`).

**Request Headers**  
```
{
    'Referer': 'https://www.yikyak.com/'
}
```

**Request Body** (JSON)  
```
{
    'countryCode': "ABC",
    'phoneNumber': "1234567890",
    'pin': "123456",
}
```

**Response** (JSON)  
Authentication token string

####Country Codes
Country codes are as follows. It appears that either the two or three character codes can be used:

|Country|Short Code|Long Code
|---|---|---
|Afghanistan|AF|AFG
|Albania|AL|ALB
|Algeria|DZ|DZA
|American Samoa|AS|ASM
|Andorra|AD|AND
|Angola|AO|AGO
|Anguilla|AI|AIA
|Antigua and Barbuda|AG|ATG
|Argentina|AR|ARG
|Armenia|AM|ARM
|Aruba|AW|ABW
|Australia|AU|AUS
|Austria|AT|AUT
|Azerbaijan|AZ|AZE
|Bahamas|BS|BHS
|Bahrain|BH|BHR
|Bangladesh|BD|BGD
|Barbados|BB|BRB
|Belarus|BY|BLR
|Belgium|BE|BEL
|Belize|BZ|BLZ
|Benin|BJ|BEN
|Bermuda|BM|BMU
|Bhutan|BT|BTN
|Bolivia|BO|BOL
|Bosnia and Herzegovina|BA|BIH
|Botswana|BW|BWA
|Brazil|BR|BRA
|Brunei Darussalam|BN|BRN
|Bulgaria|BG|BGR
|Burkina Faso|BF|BFA
|Burundi|BI|BDI
|Cambodia|KH|KHM
|Cameroon|CM|CMR
|Canada|CA|CAN
|Cape Verde|CV|CPV
|Cayman Islands|KY|CYM
|Central African Republic|CF|CAF
|Chad|TD|TCD
|Chile|CL|CHL
|China|CN|CHN
|Colombia|CO|COL
|Comoros|KM|COM
|Congo|CG|COG
|Congo, The Democratic Republic Of The|CD|COD
|Cook Islands|CK|COK
|Costa Rica|CR|CRI
|Croatia|HR|HRV
|Dominican Republic|DO|DOM
|Ecuador|EC|ECU
|Egypt|EG|EGY
|El Salvador|SV|SLV
|Equatorial Guinea|GQ|GNQ
|Eritrea|ER|ERI
|Estonia|EE|EST
|Ethiopia|ET|ETH
|Falkland Islands (Malvinas)|FK|FLK
|Faroe Islands|FO|FRO
|Fiji|FJ|FJI
|Finland|FI|FIN
|France|FR|FRA
|French Guiana|GF|GUF
|French Polynesia|PF|PYF
|Gabon|GA|GAB
|Gambia|GM|GMB
|Georgia|GE|GEO
|Germany|DE|DEU
|Ghana|GH|GHA
|Gibraltar|GI|GIB
|Greece|GR|GRC
|Greenland|GL|GRL
|Grenada|GD|GRD
|Guadeloupe|GP|GLP
|Guam|GU|GUM
|Guatemala|GT|GTM
|Guinea|GN|GIN
|Guinea-Bissau|GW|GNB
|Guyana|GY|GUY
|Haiti|HT|HTI
|Honduras|HN|HND
|Hong Kong|HK|HKG
|Hungary|HU|HUN
|Iceland|IS|ISL
|India|IN|IND
|Indonesia|ID|IDN
|Iran, Islamic Republic Of|IR|IRN
|Iraq|IQ|IRQ
|Ireland|IE|IRL
|Israel|IL|ISR
|Italy|IT|ITA
|Jamaica|JM|JAM
|Japan|JP|JPN
|Jordan|JO|JOR
|Kazakhstan|KZ|KAZ
|Kenya|KE|KEN
|Kiribati|KI|KIR
|Korea, Republic of|KR|KOR
|Kuwait|KW|KWT
|Kyrgyzstan|KG|KGZ
|Lao People's Democratic Republic|LA|LAO
|Latvia|LV|LVA
|Lebanon|LB|LBN
|Lesotho|LS|LSO
|Liberia|LR|LBR
|Libyan Arab Jamahiriya|LY|LBY
|Liechtenstein|LI|LIE
|Lithuania|LT|LTU
|Luxembourg|LU|LUX
|Macao|MO|MAC
|Macedonia, the Former Yugoslav Republic Of|MK|MKD
|Madagascar|MG|MDG
|Malawi|MW|MWI
|Malaysia|MY|MYS
|Maldives|MV|MDV
|Mali|ML|MLI
|Malta|MT|MLT
|Marshall Islands|MH|MHL
|Martinique|MQ|MTQ
|Mauritania|MR|MRT
|Mauritius|MU|MUS
|Mayotte|YT|MYT
|Mexico|MX|MEX
|Micronesia, Federated States Of|FM|FSM
|Moldova, Republic of|MD|MDA
|Monaco|MC|MCO
|Mongolia|MN|MNG
|Montenegro|ME|MNE
|Montserrat|MS|MSR
|Morocco|MA|MAR
|Mozambique|MZ|MOZ
|Myanmar|MM|MMR
|Namibia|NA|NAM
|Nauru|NR|NRU
|Nepal|NP|NPL
|Netherlands|NL|NLD
|New Caledonia|NC|NCL
|New Zealand|NZ|NZL
|Nicaragua|NI|NIC
|Niger|NE|NER
|Nigeria|NG|NGA
|Niue|NU|NIU
|Norfolk Island|NF|NFK
|Northern Mariana Islands|MP|MNP
|Norway|NO|NOR
|Oman|OM|OMN
|Pakistan|PK|PAK
|Palau|PW|PLW
|Palestinian Territory, Occupied|PS|PSE
|Panama|PA|PAN
|Papua New Guinea|PG|PNG
|Paraguay|PY|PRY
|Peru|PE|PER
|Philippines|PH|PHL
|Poland|PL|POL
|Portugal|PT|PRT
|Puerto Rico|PR|PRI
|Qatar|QA|QAT
|Saint Helena|SH|SHN
|Saint Kitts And Nevis|KN|KNA
|Saint Lucia|LC|LCA
|Saint Pierre And Miquelon|PM|SPM
|Saint Vincent And The Grenedines|VC|VCT
|Samoa|WS|WSM
|San Marino|SM|SMR
|Sao Tome and Principe|ST|STP
|Saudi Arabia|SA|SAU
|Senegal|SN|SEN
|Serbia|RS|SRB
|Seychelles|SC|SYC
|Sierra Leone|SL|SLE
|Singapore|SG|SGP
|Slovakia|SK|SVK
|Slovenia|SI|SVN
|Solomon Islands|SB|SLB
|Somalia|SO|SOM
|South Africa|ZA|ZAF
|Spain|ES|ESP
|Sri Lanka|LK|LKA
|Sudan|SD|SDN
|Suriname|SR|SUR
|Svalbard And Jan Mayen|SJ|SJM
|Sweden|SE|SWE
|Switzerland|CH|CHE
|Syrian Arab Republic|SY|SYR
|Taiwan, Province Of China|TW|TWN
|Tajikistan|TJ|TJK
|Tanzania, United Republic of|TZ|TZA
|Thailand|TH|THA
|Timor-Leste|TL|TLS
|Togo|TG|TGO
|Tokelau|TK|TKL
|Tonga|TO|TON
|Trinidad and Tobago|TT|TTO
|Tunisia|TN|TUN
|Turkey|TR|TUR
|Turkmenistan|TM|TKM
|Turks and Caicos Islands|TC|TCA
|Tuvalu|TV|TUV
|Uganda|UG|UGA
|Ukraine|UA|UKR
|United Arab Emirates|AE|ARE
|United Kingdom|GB|GBR
|United States|US|USA
|Uruguay|UY|URY
|Uzbekistan|UZ|UZB
|Vanuatu|VU|VUT
|Venezuela, Bolivarian Republic of|VE|VEN
|Viet Nam|VN|VNM
|Virgin Islands, British|VG|VGB
|Virgin Islands, U.S.|VI|VIR
|Wallis and Futuna|WF|WLF
|Yemen|YE|YEM
|Zambia|ZM|ZMB
|Zimbabwe|ZW|ZWE


###Automatic PIN Code Retrieval
`POST https://www.yikyak.com/api/auth/initPairing`

If you know your Yik Yak user ID, we avoid having to manually check the app by automatically retrieving the PIN from the API.

**Request Body**
```
{
    'userID': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
}
```

**Response**
```
{
    'pin': '110786'
    'ttl': 60,
}
```

###Refreshing Access Token
`POST https://www.yikyak.com/api/auth/token/refresh`

**Request Headers**
```
{
    'Referer': 'https://www.yikyak.com/',
    'x-access-token': <auth_token>,
}
```

**Response**
New auth token

##Authenticated Operations

Once we have retrieved the authentication token, we can interact with the API.

For all authenticated operations, the following headers must be sent:

```
{
    'Referer': 'https://www.yikyak.com/',
    'x-access-token': <auth_token>,
}
```
 


###Yakker
`GET https://www.yikyak.com/api/proxy/v1/yakker`  

**Response**
```
{
    'amplitudeID': <string>,
    'myHerd': {
        'eligible': <bool>,
        'enabled': <bool>,
        'lat': <string>,
        'long': <string>,
        'name': <string>,
    },
    'userID': <string>,
    'verificationStatus': {
        'forceVerification': <bool>,
        'isVerified': <bool>,
    },
    'yakarma': 
}
```

###New / Hot Yak Feed
`GET https://www.yikyak.com/api/proxy/v1/messages/all/new`  
`GET https://www.yikyak.com/api/proxy/v1/messages/all/hot`  

**Query String**
```
userLat=0
userLong=0
lat=<latitude>
long=<longitude>
```

`userLat` and `userLong` do not appear to be required. `lat` and `long` is the co-ordinates to retrieve Yaks from.

**Response**  
Returns up to 200(?) Yak objects

###Compose a Yak
`POST https://www.yikyak.com/api/proxy/v1/messages`

####Request Parameters
|Key|Value Type|Description
|---|---|---|
|`lat`|float|Latitude to post to
|`long`|float|Longitude to post to
|`userLat`|float|No noticeable effect; set to `0`
|`userLong`|float|No noticeable effect; set to `0`

####Request Body

|Key|Value Type|Description
|---|---|---|
|`message`|string|Contents of the Yak to submit
|`handle`|bool|Display your handle?

> **Note**
> `handle` is currently optional and defaults to `false`

###Yak Details
`GET https://www.yikyak.com/api/proxy/v1/messages/<yak_id>`

> **Note**
> The `/` in the Yak's ID must be made URL-safe i.e. converted to `%2F`
> `R%2Fxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Query String**  
These values must be sent, but appear to have no effect.  
```
userLat=0.0
userLong=0.0
```

**Response**  
Returns a JSON Yak object (see above)


###Voting on a Yak

`PUT https://www.yikyak.com/api/proxy/v1/messages/<yak_id>/upvote`  
`PUT https://www.yikyak.com/api/proxy/v1/messages/<yak_id>/downvote`  

> **Note**
> The `/` in the Yak's ID must be made URL-safe i.e. converted to `%2F`
> `R%2Fxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Query String**  
These values must be sent, but appear to have no effect.  
```
userLat=0.0
userLong=0.0
```

**Response**  
JSON parse fails on the response. Probably a malformed Yak object.

###Delete a Yak
`DELETE https://www.yikyak.com/api/proxy/v1/messages/<yak_id>`

> **Note**
> The `/` in the Yak's ID must be made URL-safe i.e. converted to `%2F`
> `R%2Fxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Query String**  
These values must be sent, but appear to have no effect.  
```
userLat=0.0
userLong=0.0
```

###Report a Yak
`PUT https://www.yikyak.com/api/proxy/v1/messages/<yak_id>/report`

> **Note**
> The `/` in the Yak's ID must be made URL-safe i.e. converted to `%2F`
> `R%2Fxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Query String**  
These values must be sent, but appear to have no effect.  
```
userLat=0.0
userLong=0.0
```

**Request Body**
```
{
    "block": <bool>,
    "reason": <string>,
}
```

Selecting to block the poster of a Yak will prevent you from ever seeing their Yaks and is irreversible. Not recommended.

Reason must be one of the following: `Offensive`, `Other`, `Spam`, `Targeting`

###Check Handle Availability
`GET https://www.yikyak.com/api/proxy/v1/yakker/handles`

####Request Parameters
|Key|Value Type|Description
|---|---|---|
|`handle`|string|Handle to claim

####JSON Response
|Key|Value Type|Description
|---|---|---|
|`code`|int|`0` success; `1` invalid; `2` taken

###Claim Handle
`POST https://www.yikyak.com/api/proxy/v1/yakker/handles`

####Request Body
|Key|Value Type|Description
|---|---|---|
|`handle`|string|Handle to claim

####JSON Response
|Key|Value Type|Description
|---|---|---|
|`code`|int|`0` success; `1` invalid; `2` taken


