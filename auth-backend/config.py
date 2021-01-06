import os

MAX_SAFE_STRING_LEN	= 512
AUTH_SERVER_NAME	= os.environ["AUTH_SERVER"]
TOKEN_LEN		= 16
TOKEN_LEN_HEX		= 32
INTROSPECT_URL		= "https://"+ AUTH_SERVER_NAME + "/auth/v1/token/introspect"
SERVER_CERTIFICATE	= "resource-server.p12"
RECORD_SRC_DIR          = '/root/datasetu-video-server/nginx/record/'
RECORD_TAR_DIR          = '/root/datasetu-video-server/nginx/record'
HLS_SRC_DIR             = '/root/datasetu-video-server/nginx/storage/rtmp+hls'

