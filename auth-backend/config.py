import os

MAX_SAFE_STRING_LEN	= 512
AUTH_SERVER_NAME	= os.environ["AUTH_SERVER"]
TOKEN_LEN_HEX		= 32
INTROSPECT_URL		= "https://"+ AUTH_SERVER_NAME + "/auth/v1/token/introspect"
RS_CERT_FILE	    = "/root/auth-backend/resource-server.pem"
RS_KEY_FILE	        = "/root/auth-backend/resource-server.key.pem"
RECORD_SRC_DIR      = '/root/datasetu-video-server/nginx/record'
RECORD_DEST_DIR     = '/root/datasetu-video-server/nginx/record/'
HLS_SRC_DIR         = '/root/datasetu-video-server/nginx/storage/rtmp+hls'
HLS_DEST_DIR         = '/root/datasetu-video-server/nginx/storage/rtmp+hls/'
