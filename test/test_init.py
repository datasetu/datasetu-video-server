import requests, sys, os, youtube_dl, json
from urllib.parse import quote_plus
import test_config as cnf, test_video_server


def auth_setup():
    requests.post(
        url=cnf.provider_url,
        verify=False,
        cert=cnf.provider_credentials,
        data=cnf.provider_body,
        headers={"content-type": "application/json"}
    )

    resp = requests.post(
        url=cnf.consumer_url,
        verify=False,
        cert=cnf.consumer_credentials,
        data=cnf.consumer_body,
        headers={"content-type": "application/json", "Host": "auth.local"}
    )
    return resp.json()


def download_videos():
    ydl_opts = {'outtmpl': '%(id)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=wKWldDnCZQ0', 'https://www.youtube.com/watch?v=QXOXIMgHgZ0',
                      'https://www.youtube.com/watch?v=od5nla42Jvc'])


if __name__ == '__main__':
    response = auth_setup()
    download_videos()
    for i in range(len(cnf.ids)):
        cnf.ids[i] = quote_plus(cnf.ids[i])

    token = quote_plus(response['token'])
    test_video_server.test_record_length(token)
    test_video_server.test_token(token)
    test_video_server.test_id(token)
    test_video_server.test_hd_video(token)
    test_video_server.test_load(token)
    test_video_server.test_hls(token)
    os.remove('wKWldDnCZQ0.webm')
    os.remove('QXOXIMgHgZ0.mkv')
    os.remove('od5nla42Jvc.webm')