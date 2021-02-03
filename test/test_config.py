import json

RESOURCE_ID = {
    1: "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-1",
    2: "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-2",
    3: "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-3",
    "public": "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource.public"
               }

YOUTUBE_URL_1 = 'https://www.youtube.com/watch?v=wKWldDnCZQ0'
YOUTUBE_URL_2 = 'https://www.youtube.com/watch?v=QXOXIMgHgZ0'
YOUTUBE_URL_3 = 'https://www.youtube.com/watch?v=od5nla42Jvc'

VIDEOS = {
    1 : 'wKWldDnCZQ0.webm',
    2 : 'QXOXIMgHgZ0.mkv',
    "HD" : 'od5nla42Jvc.webm'
        }

RTMP_HLS = 'rtmp+hls'
RTMP ='rtmp'

RECORD_SRC_DIR = '../nginx/record/'

ACL_SET_ENDPOINT = 'https://localhost:8443/auth/v1/acl/set'
ACL_SET_CERTIFICATE = '../datasetu-ca/provider/provider.pem'
ACL_SET_KEY = '../datasetu-ca/provider/provider.key.pem'
ACL_SET_CREDENTIALS = (ACL_SET_CERTIFICATE, ACL_SET_KEY)

REQUEST_TOKEN_ENDPOINT = "https://localhost:8443/auth/v1/token"
REQUEST_TOKEN_CERTIFICATE = '../datasetu-ca/consumer/consumer.pem'
REQUEST_TOKEN_KEY = '../datasetu-ca/consumer/consumer.key.pem'
REQUEST_TOKEN_CREDENTIALS = (REQUEST_TOKEN_CERTIFICATE, REQUEST_TOKEN_KEY)
REQUEST_TOKEN_BODY = json.dumps({
    "request": [
        {
            "id": RESOURCE_ID[1],
            "scopes": ["write", "read"]
        },
        {
            "id": RESOURCE_ID[2],
            "scopes": ["write", "read"]
        },
        {
            "id": RESOURCE_ID[3],
            "scopes": ["write", "read"]
        },
        {
            "id": RESOURCE_ID["public"],
            "scopes": ["write"]
        }
    ]
})
