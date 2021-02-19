import requests, youtube_dl, json, random
from urllib.parse import quote_plus
import test_config as cnf, test_video_server, test_authenticator


def auth_setup():
    ACL_SET_POLICY = ""
    for i in range(1, random.randint(5, 12)):
        ACL_SET_POLICY += "consumer@iisc.ac.in can access example.com/test-category/test-resource-" + str(i) + " for 1 month;"
    ACL_SET_POLICY += "consumer@iisc.ac.in can access example.com/test-category/test-resource.public for 1 month"

    ACL_SET_BODY = json.dumps(
        {
            "policy": ACL_SET_POLICY
        }
    )
    requests.post(
        url = cnf.ACL_SET_ENDPOINT,
        verify = False,
        cert = cnf.ACL_SET_CREDENTIALS,
        data = ACL_SET_BODY,
        headers = {"content-type": "application/json"}
    )

    resp = requests.post(
        url=cnf.REQUEST_TOKEN_ENDPOINT,
        verify=False,
        cert=cnf.REQUEST_TOKEN_CREDENTIALS,
        data=cnf.REQUEST_TOKEN_BODY,
        headers={"content-type": "application/json", "Host": "auth.local"}
    )
    return resp.json()


def download_videos():
    ydl_opts = {'outtmpl': '%(id)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([cnf.YOUTUBE_URL_1,cnf.YOUTUBE_URL_2,cnf.YOUTUBE_URL_3, cnf.YOUTUBE_URL_4])


if __name__ == '__main__':

    response = auth_setup()
    # download_videos()
    cnf.RESOURCE_ID[1] = quote_plus(cnf.RESOURCE_ID[1])
    cnf.RESOURCE_ID[2] = quote_plus(cnf.RESOURCE_ID[2])
    cnf.RESOURCE_ID[3] = quote_plus(cnf.RESOURCE_ID[3])

    token = quote_plus(response['token'])

    #**********Testing Authenticator**************
    # test_authenticator.test_is_string_safe(token)
    # test_authenticator.test_is_valid_token(token)
    # test_authenticator.test_symlink(token)
    # test_authenticator.test_auth(token)

    #**********Testing Video Server***************
    # test_video_server.test_record_length(token)
    test_video_server.test_token(token)
    test_video_server.test_id(token)
    test_video_server.test_hd_video(token)
    test_video_server.test_load(token)
    # test_video_server.test_hls(token)
    # test_video_server.test_live_stream(token)
    # for i in cnf.VIDEOS:
    #     os.remove(i)
