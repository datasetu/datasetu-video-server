import json

RESOURCE_ID = {
    1: "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-1",
    2: "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-2",
    3: "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-3",
    4: "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-4",
    # "public": "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource.public"
               }

YOUTUBE_URL_1 = 'https://www.youtube.com/watch?v=61QSHrOuGEA'
YOUTUBE_URL_2 = 'https://www.youtube.com/watch?v=wKWldDnCZQ0'
YOUTUBE_URL_3 = 'https://www.youtube.com/watch?v=QXOXIMgHgZ0'
YOUTUBE_URL_4 = 'https://www.youtube.com/watch?v=R3GfuzLMPkA'

VIDEOS = {
    1 : '61QSHrOuGEA.mkv',
    2 : 'wKWldDnCZQ0.webm',
    3 : 'QXOXIMgHgZ0.mkv',
    "HD" : 'R3GfuzLMPkA.webm'
        }

RTMP_HLS = 'rtmp+hls'
RTMP ='rtmp'
PUSH_VALID = 'push_valid'
PUSH_INVALID = 'push_invalid'
PLAY_VALID = 'play_valid'
PLAY_INVALID = 'play_invalid'
FRAME_RATE = 'frame_rate'

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
            "id": RESOURCE_ID[4],
            "scopes": ["write", "read"]
        },
        # {
        #     "id": RESOURCE_ID["public"],
        #     "scopes": ["write"]
        # }
    ]
})

INTROSPECT_ENDPOINT = "https://localhost:8443/auth/v1/token/introspect"

LIVE_STREAM = 'rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream'
