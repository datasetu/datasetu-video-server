from __future__ import print_function

__author__ = "Vishwajeet Mishra <vishwajeet@artpark.in>"

# Purpose: Main application file
import json, os
from flask import Flask, request, Response
from urllib.parse import unquote_plus, quote_plus, urlparse
from requests import post
import datetime
import config
import sys
import watchdog.events
import watchdog.observers


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.flv'],
                                                             ignore_directories=True, case_sensitive=False)

    def on_created(self, event):
        src = event.src_path

        if "%252F" not in src:
            return

        record_name = src.split("record/")[1]
        target = config.RECORD_TAR_DIR
        record_name_split = record_name.split("%252F")

        for segment in range(len(record_name_split) - 1):
            target += "/" + record_name_split[segment]

            if not os.path.exists(target):
                os.makedirs(target)

        recording_unique_id_split = record_name_split[-1].split("-")

        if len(recording_unique_id_split) == 2:
            target += '/' + recording_unique_id_split[0]

            if not os.path.exists(target):
                os.makedirs(target)

            target += '/' + recording_unique_id_split[1]

            if not os.path.islink(target):
                os.symlink(src, target)


app = Flask(__name__, template_folder='.')

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
    # issued_to		= split[1]
    random_hex = split[1]

    if (issued_by != config.AUTH_SERVER_NAME):
        return False

    if (len(random_hex) != config.TOKEN_LEN_HEX):
        return False

    return True


def symlink(resource_id):
    resource_id_split = resource_id.split('/')

    hls_src_dir = config.HLS_SRC_DIR

    src = hls_src_dir + '/' + quote_plus(resource_id)

    for segment in range(len(resource_id_split) - 1):
        hls_src_dir += '/' + resource_id_split[segment]

        if not os.path.exists(hls_src_dir):
            os.makedirs(hls_src_dir)

    hls_src_dir += '/' + resource_id_split[-1]

    if not os.path.islink(hls_src_dir):
        os.symlink(src, hls_src_dir)


def auth(introspect_response, resource_id, call):
    if (not isinstance(introspect_response, dict) or not introspect_response or 'request' not in introspect_response):
        print("Request not found in body.", file=sys.stderr)
        return False

    for r in introspect_response['request']:
        if (not r['scopes']):
            print("Scopes not found in body.", file=sys.stderr)
            return False

        if (r['id'] != resource_id):
            continue

        if (call == 'play'):
            if ("read" not in r['scopes']):
                print("Read scope is not assigned.", file=sys.stderr)
                return False

        elif (call == 'publish'):
            if ("write" not in r['scopes']):
                print("Write Scope is not assigned.", file=sys.stderr)
                return False

            split = resource_id.split("/")

            if (len(split) > 7):
                print("Request id too long", file=sys.stderr)
                return False

        else:
            print("Invalid Call")
            return False

        return True
    return False


def validation(resource_id, token, call):
    if (not is_valid_token(token)):
        print("Invalid Token", file=sys.stderr)
        return Response(status=403)

    if (token in token_cache):

        token_expiry = datetime.datetime.strptime(token_cache[token]['expiry'], '%Y-%m-%dT%H:%M:%S.%fZ')

        if (token_expiry < datetime.datetime.now()):
            token_cache.pop(token)
        else:
            if (auth(token_cache[token], resource_id, call)):
                symlink(resource_id)
                return Response(status=200)
            return Response(status=403)

    body = {'token': token}

    response = post(
        url=config.INTROSPECT_URL,
        headers={"content-type": "application/json"},
        data=json.dumps(body),
        cert=(config.RS_CERT_FILE, config.RS_KEY_FILE),
        verify=False
    )
    if (response.status_code != 200):
        return Response(status=response.status_code)
    token_cache[token] = response.json()
    if (auth(response.json(), resource_id, call)):
        symlink(resource_id)
        return Response(status=200)
    return Response(status=403)


@app.route('/api/on-hls-auth', methods=['GET'])
def on_hls_auth() -> Response:
    """
        API to authenticate on_hls_subcription
        :return:
            Response: status_code(200,403)
    """
    if ('HTTP_URL' not in request.environ
            or 'HTTP_TOKEN' not in request.environ
            or len(request.environ['HTTP_TOKEN']) == 0):
        print('Invalid Input', file=sys.stderr)
        return Response(status=403)

    uri = urlparse(request.environ['HTTP_URL'])
    path_split = uri.path.split('/')

    if len(path_split) != 4:
        print("Invalid ID", file=sys.stderr)
        return Response(status=403)

    resource_id = unquote_plus(path_split[2])
    token = unquote_plus(request.environ['HTTP_TOKEN'])
    call = 'play'

    return validation(resource_id, token, call)


@app.route("/api/on-live-auth", methods=['POST'])
def on_live_auth() -> Response:
    """
    API to authenticate on_publish
    :return:
        Response: status_code(200,403)
    """
    token = request.form['token']
    resource_id = unquote_plus(request.form['name'])
    call = request.form['call']

    return validation(resource_id, token, call)


if __name__ == '__main__':
    src_path = config.RECORD_SRC_DIR
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    app.run(threaded=True, port=3001, host='0.0.0.0')
