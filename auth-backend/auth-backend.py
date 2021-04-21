from __future__ import print_function

__author__ = "Vishwajeet Mishra <vishwajeet@artpark.in>"

# Purpose: Main application file
from flask import Flask, request, Response
from urllib.parse import unquote_plus, urlparse
import config, utils
import sys, logging
import watchdog.observers


app = Flask(__name__)


# TODO: Use Managed Cache library

@app.route('/api/on-hls-auth', methods=['GET'])
def on_hls_auth() -> Response:
    """
        API to authenticate on_hls_subcription:
        input:
            Request:
                request.environ contains 'HTTP_URL' and 'HTTP_TOKEN'
                'HTTP_URL': '/rtmp+hls/<encoded-resource-id>/index.m3u8'
                'HTTP_TOKEN': '<encoded-token>'
        return:
            Response: status_code(200,403)
    """

    if ('HTTP_URL' not in request.environ
            or 'HTTP_TOKEN' not in request.environ
            or len(request.environ['HTTP_TOKEN']) == 0):
        logging.info('Invalid Input', file=sys.stderr)
        return Response(status=403)

    uri = urlparse(request.environ['HTTP_URL'])
    path_split = uri.path.split('/')

    # TODO: Add detailed comments
    if len(path_split) != 4:
        logging.info("Invalid ID", file=sys.stderr)
        return Response(status=403)

    resource_id = unquote_plus(path_split[2])
    token = unquote_plus(request.environ['HTTP_TOKEN'])
    request_type = 'play'

    return Response(status=200 if utils.validation(resource_id, token, request_type) else 400)


@app.route("/api/on-live-auth", methods=['POST'])
def on_live_auth() -> Response:
    """
    API to authenticate on_publish
    :return:
        Response: status_code(200,403)
    """
    if (not request or 'token' not in request.form or 'name' not in request.form or 'call' not in request.form):
        return Response(status=403)

    token = request.form['token']
    resource_id = unquote_plus(request.form['name'])
    request_type = request.form['call']

    return Response(status=200 if utils.validation(resource_id, token, request_type) else 400)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    src_path = config.RECORD_SRC_DIR
    event_handler = utils.Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=False)
    observer.start()
    app.run(threaded=True, port=3001, host='0.0.0.0', debug=True)

    # TODO: ADD WSGI
    # http_server =   WSGIServer(('0.0.0.0', 3001), app, keyfile = 'ssl/privkey.pem', certfile='ssl/fullchain.pem')
