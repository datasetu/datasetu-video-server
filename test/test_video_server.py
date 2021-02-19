import subprocess, sys, test_config as cnf, requests
from multiprocessing import Process, Manager
from time import sleep
import vlc
import pyinotify
import util


def test_record_length(token):

    multitask = util.Multitask()

    src_path = cnf.RECORD_SRC_DIR
    wm = pyinotify.WatchManager()
    wm.add_watch(src_path, pyinotify.IN_CLOSE_WRITE, util.inCloseWrite)
    notifier = pyinotify.Notifier(wm)
    publisher = util.Ffmpeg()
    publisher.input(cnf.VIDEOS[1])
    publisher.output(util.get_rtmp_path(cnf.RTMP_HLS, cnf.RESOURCE_ID[1], token),'f','flv')
    multitask.add(notifier.loop)
    multitask.add(publisher.push,cnf.PUSH_VALID)
    multitask.run()


def test_token(token):
    # publisher = util.Ffmpeg()
    # publisher.input(cnf.VIDEOS[1])
    # publisher.output(util.get_rtmp_path(cnf.RTMP, cnf.RESOURCE_ID[1], token) ,'f', 'flv')
    # publisher.push({},cnf.PUSH_VALID)
    # medai = vlc.MediaPlayer(util.get_rtmp_path(cnf.RTMP, cnf.RESOURCE_ID[1], token))
    # medai.play()


    incorrect_token = util.generate_random_chars()
    multitask = util.Multitask()
    # ***************when publisher has verified token*************
    for type in [cnf.RTMP, cnf.RTMP_HLS]:
        publisher = util.Ffmpeg()
        publisher.input(cnf.VIDEOS[1])
        publisher.output(util.get_rtmp_path(type, cnf.RESOURCE_ID[1], token) ,'f', 'flv')

        subscriber_1 = util.Ffmpeg()
        subscriber_1.input(util.get_rtmp_path(type, cnf.RESOURCE_ID[1], token))

        subscriber_2 = util.Ffmpeg()
        subscriber_2.input(util.get_rtmp_path(type, cnf.RESOURCE_ID[1], incorrect_token))

        multitask.add(publisher.push,cnf.PUSH_VALID)
        multitask.add(subscriber_1.play,cnf.PLAY_VALID, 20)
        multitask.add(subscriber_2.play,cnf.PLAY_INVALID, 20)

    # ***************when publisher has incorrect token*************
    for type in [cnf.RTMP,cnf.RTMP_HLS]:
        publisher = util.Ffmpeg()
        publisher.input(cnf.VIDEOS[1])
        publisher.output(util.get_rtmp_path(type, cnf.RESOURCE_ID[2], incorrect_token), 'f', 'flv')

        subscriber_1 = util.Ffmpeg()
        subscriber_1.input(util.get_rtmp_path(type, cnf.RESOURCE_ID[2], token))

        subscriber_2 = util.Ffmpeg()
        subscriber_2.input(util.get_rtmp_path(type, cnf.RESOURCE_ID[2], incorrect_token))

        multitask.add(publisher.push, cnf.PUSH_INVALID)
        multitask.add(subscriber_1.play, cnf.PLAY_VALID, 20)
        multitask.add(subscriber_2.play, cnf.PLAY_INVALID, 20)

    multitask.run()

    for key, value in multitask.return_dict.items():
        if 'invalid' in key:
            assert (value is False)
        else:
            assert (value is True)

    print("Token test passed!", file=sys.stderr)


def test_id(token):

    incorrect_id = util.generate_random_chars()
    multitask = util.Multitask()

    # ***************when publisher has verified id*************
    for type in [cnf.RTMP, cnf.RTMP_HLS]:
        publisher = util.Ffmpeg()
        publisher.input(cnf.VIDEOS[1])
        publisher.output(util.get_rtmp_path(type, cnf.RESOURCE_ID[1], token), 'f', 'flv')

        subscriber_1 = util.Ffmpeg()
        subscriber_1.input(util.get_rtmp_path(type, cnf.RESOURCE_ID[1], token))

        subscriber_2 = util.Ffmpeg()
        subscriber_2.input(util.get_rtmp_path(type, incorrect_id, token))

        multitask.add(publisher.push, cnf.PUSH_VALID)
        multitask.add(subscriber_1.play, cnf.PLAY_VALID, 20)
        multitask.add(subscriber_2.play, cnf.PLAY_INVALID, 20)

    # ***************when publisher has incorrect id*************
    for type in [cnf.RTMP, cnf.RTMP_HLS]:
        publisher = util.Ffmpeg()
        publisher.input(cnf.VIDEOS[1])
        publisher.output(util.get_rtmp_path(type, incorrect_id, token), 'f', 'flv')

        subscriber_1 = util.Ffmpeg()
        subscriber_1.input(util.get_rtmp_path(type, cnf.RESOURCE_ID[2], token))

        subscriber_2 = util.Ffmpeg()
        subscriber_2.input(util.get_rtmp_path(type, incorrect_id, token))

        multitask.add(publisher.push, cnf.PUSH_INVALID)
        multitask.add(subscriber_1.play, cnf.PLAY_VALID, 20)
        multitask.add(subscriber_2.play, cnf.PLAY_INVALID, 20)

    multitask.run()

    for key, value in multitask.return_dict.items():
        if 'invalid' in key:
            assert (value is False)
        else:
            assert (value is True)

    print("Id test passed!", file=sys.stderr)


def test_hd_video(token):
    # TODO: Check resolution, size, duration etc
    result = Manager().dict()
    publisher = util.Ffmpeg()
    publisher.input(cnf.VIDEOS["HD"])
    publisher.output(util.get_rtmp_path(cnf.RTMP, cnf.RESOURCE_ID[1], token), 'f', 'flv')
    publisher.push( result, cnf.PUSH_VALID, 20)
    assert (result[cnf.PUSH_VALID] is True)

    print("Hd test passed!", file=sys.stderr)


def test_load(token):

    multitask = util.Multitask()
    # ***************when publisher has verified token*************
    for type in [cnf.RTMP, cnf.RTMP_HLS]:
        for id in cnf.RESOURCE_ID.values():
            publisher = util.Ffmpeg()
            publisher.input(cnf.VIDEOS[1])
            publisher.output(util.get_rtmp_path(type, id, token), 'f', 'flv')

            subscriber = util.Ffmpeg()
            subscriber.input(util.get_rtmp_path(type, id, token))

            multitask.add(publisher.push, cnf.PUSH_VALID, 20)
            multitask.add(subscriber.play, cnf.PLAY_VALID, 20)
    multitask.run()
    print(len(multitask.return_dict))
    for res in multitask.return_dict.values():
        assert(res is True)

    print('Load test passed!', file=sys.stderr)


def test_hls(token):

    publisher = util.Ffmpeg()
    publisher.input(cnf.VIDEOS[1])
    publisher.output(util.get_rtmp_path(cnf.RTMP_HLS, cnf.RESOURCE_ID[1], token), 'f', 'flv')
    publisher.push({},cnf.PUSH_VALID, 20)

    # TODO: Find a way to remove this
    sleep(60)
    response = requests.get('https://localhost:3002/rtmp+hls/' + cnf.RESOURCE_ID[1] + '/index.m3u8',
                            cookies={'token': token}, verify=False)
    assert (response.status_code == 200)
    print('HLS test passed!', file=sys.stderr)


def test_live_stream(token):

    multitask = util.Multitask()

    publisher = util.Ffmpeg()
    publisher.input(cnf.LIVE_STREAM)
    publisher.output(util.get_rtmp_path(cnf.RTMP, cnf.RESOURCE_ID[1], token), 'f', 'flv')

    subscriber = util.Ffmpeg()
    subscriber.input(util.get_rtmp_path(cnf.RTMP, cnf.RESOURCE_ID[1], token))

    multitask.add(publisher.push, cnf.PUSH_VALID, 20)
    multitask.add(subscriber.play, cnf.PLAY_VALID, 20)
    multitask.run()

    for res in multitask.return_dict.values():
        assert(res is True)

    print("Live Stream Test passed!")

