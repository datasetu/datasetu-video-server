__author__ = "Vishwajeet Mishra <vishwajeet@artpark.in"
# Purpose: Main application file
import json
from flask import Flask, request, Response, jsonify, render_template
from urllib.parse import unquote_plus
from requests_pkcs12 import post
import datetime
import config
app = Flask(__name__,template_folder='.')

token_cache={}

def is_valid_email (email):
	if (not email or type(email) == str):
		return False

	if (len(email) < 5 or len(email) > 64):
		return False

	# reject email ids starting with invalid chars
	invalid_start_chars = ".-_@"

	if (invalid_start_chars.index(email[0]) != -1):
		return False

	split = email.split("@")

	if (len(split) != 2):
		return False

	user = split[0]; # the login email

	if (len(user) == 0 or len(user) > 30):
		return False

	num_dots = 0

	for chr in email:

		if (
				(chr >= "a" and chr <= "z") or
				(chr >= "A" and chr <= "Z") or
				(chr >= "0" and chr <= "9") or
				chr == "-" or chr == "_" or chr == "@"):
			continue
		if(chr=="."):
			num_dots += 1
		else:
			return False

	if (num_dots < 1):
		return False

	return True

def is_string_safe (string, exceptions = ""):
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

def is_valid_token (token, user = None):
	if (not is_string_safe(token)):
		return False

	split = token.split("/")

	if (len(split) != 2):
		return False

	issued_by		= split[0]
	# issued_to		= split[1]
	random_hex	= split[1]

	if (issued_by != config.AUTH_SERVER_NAME):
		return False

	if (len(random_hex) != config.TOKEN_LEN_HEX):
		return False

	# if (user and user != issued_to):
	# 	return False	# token was not issued to this user

	# if (not is_valid_email(issued_to)):
	# 	return False

	return True

def auth(introspect_response,id,call):
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
			if ("read" not in r['scopes']):
				print("Write Scope is not assigned.")
				return False

			split = id.split("/")

			if (len(split) > 7):
				print("Request id too long")
				return False

		return True
	return False

@app.route("/api/on-live-auth", methods=['POST'])
def on_live_auth() -> Response:
	"""
    API to authenticate on_publish
    :return:
        Response: status_code(200,400)
    """
	
	token = request.form['token']
	id = unquote_plus(request.form['name'])
	call = request.form['call']
	if (not is_valid_token(token)):
		print("Invalid Token")
		return Response(status=400)

	if (token in token_cache):

		token_expiry = datetime.datetime.strptime(token_cache[token]['expiry'],'%Y-%m-%dT%H:%M:%S.%fZ')

		if (token_expiry < datetime.datetime.now()):
			token_cache.pop(token)
		else:
			if (auth(token_cache[token], id,call)):
				return Response(status=200)
			return Response(status=400)


	body = {'token':token}

	response = post(
        url = config.INTROSPECT_URL,
        headers     = {"content-type":"application/json"},
        data=json.dumps(body),
        pkcs12_filename=config.SERVER_CERTIFICATE,
        pkcs12_password=''
    )
	if(response.status_code != 200):
		print(response.status_code)
		return Response(status=response.status_code)
	token_cache[token]=response.json()
	if(auth(response.json(),id,call)):
		return Response(status=200)
	return Response(status=400)


@app.route("/",methods=['GET'])
def welcome() -> Response:
	return render_template('index.html')

if __name__ == '__main__':
	app.run(threaded=True, port=3001, host='0.0.0.0')
