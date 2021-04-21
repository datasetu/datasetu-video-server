import json, os, sys, logging
from requests import post
import datetime
import watchdog.events
from urllib.parse import unquote_plus, quote_plus
import config


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.flv'],
                                                             ignore_directories=True, case_sensitive=False)

    def on_created(self, event):
        src = event.src_path
        logging.info(src, file=sys.stderr)
        record_name = src.split("/")[-1]
        target = config.RECORD_DEST_DIR
        record_name_split = unquote_plus(unquote_plus(record_name)).split('/')

        target += '/'.join(record_name_split[:-1])

        if not os.path.exists(target):
            os.makedirs(target)

        recording_unique_id_split = record_name_split[-1].rsplit("-", 1)

        if len(recording_unique_id_split) == 2:
            target += '/' + recording_unique_id_split[0]

            if not os.path.exists(target):
                os.makedirs(target)

            target += '/' + recording_unique_id_split[1]

            if not os.path.islink(target):
                os.symlink(src, target)

# TODO: Use a managed cache library
token_cache = {}


def is_string_safe(string, exceptions="/.@-"):
    if (not string or type(string) != str):
        return False

    if (len(string) == 0 or len(string) > config.MAX_SAFE_STRING_LEN):
        return False

    for ch in string:
        if (
                (ch >= "a" and ch <= "z") or
                (ch >= "A" and ch <= "Z") or
                (ch >= "0" and ch <= "9")
        ):
            continue

        if (exceptions.find(ch) == -1):
            return False

    return True


def is_valid_token(token):
    if (not is_string_safe(token)):
        return False

    split = token.split("/")

    if (len(split) != 2):
        return False

    issued_by = split[0]
    random_hex = split[1]

    # TODO: Check issued by against array of trusted auth servers
    if (issued_by != config.AUTH_SERVER_NAME):
        return False

    if (len(random_hex) != config.TOKEN_LEN_HEX):
        return False

    return True


def symlink(resource_id):
    resource_id_split = resource_id.split('/')

    hls_src_dir = config.HLS_SRC_DIR

    src = hls_src_dir + '/' + quote_plus(resource_id)

    dest = config.HLS_DEST_DIR + '/'.join(resource_id_split[:-1])

    if not os.path.exists(dest):
        os.makedirs(dest)

    dest += '/' + resource_id_split[-1]

    if not os.path.islink(dest):
        os.symlink(src, dest)


# TODO: we may need to include checks for additional policy variables
def auth(introspect_response, resource_id, request_type):
    if (not isinstance(introspect_response, dict) or not introspect_response or 'request' not in introspect_response):
        logging.info("Request not found in body.", file=sys.stderr)
        return False

    for r in introspect_response['request']:
        if (r['id'] != resource_id):
            continue

        if (request_type == 'play'):
            if ("read" not in r['scopes']):
                logging.info("Read scope is not assigned.", file=sys.stderr)
                return False

        elif (request_type == 'publish'):
            if ("write" not in r['scopes']):
                logging.info("Write Scope is not assigned.", file=sys.stderr)
                return False

            split = resource_id.split("/")

            # TODO: Align with aggregated Id implementation in vermillion
            if (len(split) > 7):
                logging.info("Request id too long", file=sys.stderr)
                return False

        else:
            logging.info("Invalid Call", file=sys.stderr)
            return False

        return True
    return False


def validation(resource_id, token, request_type):
    if (not is_valid_token(token)):
        logging.info("Invalid Token", file=sys.stderr)
        return False

    if (token in token_cache):

        token_expiry = datetime.datetime.strptime(token_cache[token]['expiry'], '%Y-%m-%dT%H:%M:%S.%fZ')

        if (token_expiry < datetime.datetime.now()):
            token_cache.pop(token)

        else:
            if (auth(token_cache[token], resource_id, request_type)):
                symlink(resource_id)
                return True
        return False

    body = {'token': token}

    response = post(
        url=config.INTROSPECT_URL,
        headers={"content-type": "application/json"},
        data=json.dumps(body),
        cert=(config.RS_CERT_FILE, config.RS_KEY_FILE),
        verify=(False if config.AUTH_SERVER_NAME == 'auth.local' else True)
    )
    if (response.status_code != 200):
        return False
    token_cache[token] = response.json()
    if (auth(response.json(), resource_id, request_type)):
        symlink(resource_id)
        return True
    return False
