import json,os

Local_AUTH_BASE_URL = 'https://localhost:8443/auth/v1/'

RESOURCE_ID = {
    "test-resource-1": "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-1",
    "test-resource-2": "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-2",
    "test-resource-3": "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-3",
    "test-resource-4": "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-4",
    "public": "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource.public"
}

YOUTUBE_URL = ['https://www.youtube.com/watch?v=iDO9J_3OVJ0',
               'https://www.youtube.com/watch?v=wKWldDnCZQ0',
               'https://www.youtube.com/watch?v=QXOXIMgHgZ0',
               'https://www.youtube.com/watch?v=R3GfuzLMPkA'
               ]

VIDEOS = {
    "countdown" : 'iDO9J_3OVJ0',
    "Asha" : 'wKWldDnCZQ0',
    "Artpark" : 'QXOXIMgHgZ0',
    "HD" : 'R3GfuzLMPkA'
}

RTMP_HLS = 'rtmp+hls'
RTMP = 'rtmp'
PUSH_VALID = 'push_valid'
PUSH_INVALID = 'push_invalid'
PLAY_VALID = 'play_valid'
PLAY_INVALID = 'play_invalid'
FRAME_RATE = 'frame_rate'

RECORD_SRC_DIR = '../nginx/record/'

ACL_SET_ENDPOINT = Local_AUTH_BASE_URL +'acl/set'
PROVIDER_CERTIFICATE = '../datasetu-ca/provider/provider.pem'
PROVIDER_KEY = '../datasetu-ca/provider/provider.key.pem'
PROVIDER_CREDENTIALS = (PROVIDER_CERTIFICATE, PROVIDER_KEY)

REQUEST_TOKEN_ENDPOINT = Local_AUTH_BASE_URL + "token"
CONSUMER_CERTIFICATE = '../datasetu-ca/consumer/consumer.pem'
CONSUMER_KEY = '../datasetu-ca/consumer/consumer.key.pem'
CONSUMER_CREDENTIALS = (CONSUMER_CERTIFICATE, CONSUMER_KEY)
REQUEST_TOKEN_BODY = json.dumps({
    "request": [
        {
            "id": RESOURCE_ID["test-resource-1"],
            "scopes": ["write", "read"]
        },
        {
            "id": RESOURCE_ID["test-resource-2"],
            "scopes": ["write", "read"]
        },
        {
            "id": RESOURCE_ID["test-resource-3"],
            "scopes": ["write", "read"]
        },
        {
            "id": RESOURCE_ID["test-resource-4"],
            "scopes": ["write", "read"]
        },
        {
            "id": RESOURCE_ID["public"],
            "scopes": ["read", "write"]
        }
    ]
})

INTROSPECT_ENDPOINT = Local_AUTH_BASE_URL + "token/introspect"

LIVE_STREAM = 'rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream'
