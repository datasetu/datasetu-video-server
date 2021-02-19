import os,sys,urllib.parse, ffmpeg,subprocess,json
from requests_pkcs12 import post
sys.path.insert(0, '../auth-backend')
os.environ["AUTH_SERVER"] = 'auth.local'
import app, util, test_config as cnf, config

def test_is_string_safe(token):
    token = urllib.parse.unquote_plus(token)
    assert app.is_string_safe(token) == True
    assert app.is_string_safe("") == False
    assert app.is_string_safe([]) == False
    assert app.is_string_safe({}) == False
    assert app.is_string_safe(util.generate_random_chars(special_chars=False)) == True
    assert app.is_string_safe(util.generate_random_chars(letters=False,digits=False)) == False
    assert app.is_string_safe(util.generate_random_chars(n=513, special_chars=False)) == False
    print('String Safe Test passed!')

def test_is_valid_token(token):
    token = urllib.parse.unquote_plus(token)
    assert app.is_valid_token(token) == True
    assert app.is_valid_token(util.generate_random_chars(special_chars=False)) == False

    incorrect_token = util.generate_random_chars(special_chars=False) + "/" + util.generate_random_chars(n = 32, special_chars=False)
    assert app.is_valid_token(incorrect_token) == False

    random_token = "auth.local/" + util.generate_random_chars(n=32, special_chars=False)
    assert app.is_valid_token(random_token) == True

    random_token = "auth.local/" + util.generate_random_chars(n=33, special_chars=False)
    assert app.is_valid_token(random_token) == False

    print('Valid Token Test Passed!')

def test_symlink(token):
    print('https://www.localhost:3002?id='+cnf.RESOURCE_ID[1]+"&token="+token)
    id = urllib.parse.quote_plus(cnf.RESOURCE_ID[1])
    assert os.path.islink('../nginx/storage/rtmp+hls/'+id) == False
    # sub = ffmpeg \
    #     .input(cnf.VIDEOS[1]) \
    #     .output(util.get_rtmp_path(cnf.RTMP_HLS, cnf.RESOURCE_ID[1], token), format='flv') \
    #     .run_async(
    #     pipe_stdout=True,
    #     pipe_stderr=True)
    command = ['ffmpeg',
               '-re',
               '-i', cnf.VIDEOS[1],
               '-c:v', 'libx264',
               '-preset', 'veryfast',
               '-maxrate', '3000k',
               '-bufsize', '6000k',
               '-pix_fmt', 'yuv420p',
               '-g', '50',
               '-c:a', 'aac',
               '-b:a', '160k',
               '-ac', '2',
               '-ar', '44100',
               '-f', 'flv',
               util.get_rtmp_path(cnf.RTMP_HLS,cnf.RESOURCE_ID[1],token)]
    sub = subprocess.Popen(command, shell=False, stderr=subprocess.PIPE,stdin=subprocess.PIPE
                            )
    out = sub.communicate()[1]
    print(out)
    assert os.path.islink('../nginx/storage/rtmp+hls/' + id) == True
    assert os.path.islink('../nginx/storage/rtmp+hls/'+util.generate_random_chars()) == False
    print("Symlink Test Passed!")

def test_auth(token):
    id = urllib.parse.unquote_plus(cnf.RESOURCE_ID[1])
    assert app.auth(None, id, 'play') == False
    assert app.auth(None, id, 'publish') == False

    incorrect_response = {util.generate_random_chars():util.generate_random_chars()}
    assert app.auth(incorrect_response, cnf.RESOURCE_ID[1], 'play') == False
    response = post(
        url=cnf.INTROSPECT_ENDPOINT,
        headers={"content-type": "application/json"},
        data=json.dumps({'token':urllib.parse.unquote_plus(token)}),
        pkcs12_filename='../auth-backend/'+config.SERVER_CERTIFICATE,
        pkcs12_password='',
        verify=False
    )
    assert app.auth(response.json(), id, 'play') == True
    assert app.auth(response.json(), id, 'publish') == True
    assert app.auth(response.json(), id, util.generate_random_chars()) == False

    print('Auth Test Passed!')

