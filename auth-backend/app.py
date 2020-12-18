from __future__ import print_function

__author__ = "Vishwajeet Mishra <vishwajeet@artpark.in>"

# Purpose: Main application file
import json, os
from flask import Flask, request, Response, jsonify, render_template
from urllib.parse import unquote_plus, quote_plus, urlparse, parse_qs
from requests_pkcs12 import post
import datetime
import config
import sys

app = Flask(__name__, template_folder='.')

token_cache = {}

def is_string_safe(string, exceptions=""):
    if (not string or type(string) != str):
        return False

    if (len(string) == 0 or len(string) > config.MAX_SAFE_STRING_LEN):
        return False

    exceptions = exceptions + "-/.@"

    for ch in string:
        if (
                (ch >= "a" and ch <= "z") or
                (ch >= "A" and ch <= "Z") or
                (ch >= "0" and ch <= "9")
        ):
            continue

        if (exceptions.index(ch) == -1):
            return False

    return True


def is_valid_token(token, user=None):
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


def symlink(id):
    id_split = id.split('/')

    dir = config.HLS_SCR_DIR

    src = dir + '/' + quote_plus(id)

    for segment in range(len(id_split) - 1):
        dir += '/' + id_split[segment]

        if not os.path.exists(dir):
            os.makedirs(dir)

    dir += '/' + id_split[-1]

    if not os.path.islink(dir):
        os.symlink(src, dir)


def auth(introspect_response, id, call):
    if (not introspect_response or not introspect_response['request']):
        print("Request not found in body.")
        return False

    for r in introspect_response['request']:
        if (not r['scopes']):
            print("Scopes not found in body.")
            return False

        if (r['id'] != id):
            continue

        if (call == 'play'):
            if ("read" not in r['scopes']):
                print("Read scope is not assigned.")
                return False
        else:
            if ("write" not in r['scopes']):
                print("Write Scope is not assigned.")
                return False

            split = id.split("/")

            if (len(split) > 7):
                print("Request id too long")
                return False

        return True
    return False


def validation(id, token, call):
    if (not is_valid_token(token)):
        print("Invalid Token")
        return Response(status=403)

    if (token in token_cache):

        token_expiry = datetime.datetime.strptime(token_cache[token]['expiry'], '%Y-%m-%dT%H:%M:%S.%fZ')

        if (token_expiry < datetime.datetime.now()):
            token_cache.pop(token)
        else:
            if (auth(token_cache[token], id, call)):
                symlink(id)
                return Response(status=200)
            return Response(status=403)

    body = {'token': token}

    response = post(
        url=config.INTROSPECT_URL,
        headers={"content-type": "application/json"},
        data=json.dumps(body),
        pkcs12_filename=config.SERVER_CERTIFICATE,
        pkcs12_password=''
    )
    if (response.status_code != 200):
        return Response(status=response.status_code)
    token_cache[token] = response.json()
    if (auth(response.json(), id, call)):
        symlink(id)
        return Response(status=200)
    return Response(status=403)


@app.route('/api/on-hls-auth', methods=['GET'])
def on_hls_auth() -> Response:
    """
        API to authenticate on_hls_subcription
        :return:
            Response: status_code(200,403)
        """
    if ('HTTP_X_ORIGINAL_URI' not in request.environ
        or 'HTTP_X_ORIGINAL_HEADER' not in request.environ
        or len(request.environ['HTTP_X_ORIGINAL_HEADER']) == 0):
        print('Invalid Input')
        return Response(status=403)

    uri = urlparse(request.environ['HTTP_X_ORIGINAL_URI'])
    cookie = request.environ['HTTP_X_ORIGINAL_HEADER']
    path_split = uri.path.split('/')

    if len(path_split) != 4:
        print("Invalid ID")
        return Response(status=403)

    id = unquote_plus(path_split[2])
    token = unquote_plus(cookie)
    call = 'play'

    return validation(id, token, call)


@app.route("/api/on-live-auth", methods=['POST'])
def on_live_auth() -> Response:
    """
    API to authenticate on_publish
    :return:
        Response: status_code(200,403)
    """
    token = request.form['token']
    id = unquote_plus(request.form['name'])
    call = request.form['call']

    return validation(id, token, call)


if __name__ == '__main__':
    app.run(threaded=True, port=3001, host='0.0.0.0')
