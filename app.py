__author__ = "Vishwajeet Mishra <vishwajeet@artpark.in"
# Purpose: Main application file
import json
from flask import Flask, request, Response, jsonify
from requests_pkcs12 import post
app = Flask(__name__)


@app.route("/api/on-live-auth", methods=['POST'])
def on_live_auth() -> Response:
    """
    API to authenticate on_publish
    :return:
        Response: status_code(200,400)
    """
    body={'token':request.form['token']}
    print(body)
    r = post(
        url = "https://auth.datasetu.org/auth/v1/token/introspect",
        headers     = {"content-type":"application/json"},
        data=json.dumps(body), 
        pkcs12_filename='certificate.pem.p12', 
        pkcs12_password=''
    )
    return Response(status=r.status_code)

if __name__ == '__main__':
    app.run(threaded=True, port=3001)