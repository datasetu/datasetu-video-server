#!/usr/bin/env python3

import sys, config as conf, requests
from multiprocessing import Manager
from time import sleep
import pyinotify
import utils,cv2


def test_record_length(token):

    multitask = utils.Multitask()

    src_path = conf.RECORD_SRC_DIR
    wm = pyinotify.WatchManager()
    wm.add_watch(src_path, pyinotify.IN_CLOSE_WRITE, utils.inCloseWrite)
    notifier = pyinotify.Notifier(wm)
    publisher = utils.Ffmpeg()
    publisher.input(conf.VIDEOS[1])
    publisher.output(utils.get_rtmp_path(conf.RTMP_HLS, conf.RESOURCE_ID[1], token),'-f','flv')
    multitask.add(notifier.loop)
    multitask.add(publisher.push,conf.PUSH_VALID)
    multitask.run()


def test_token(token):
    incorrect_token = utils.generate_random_chars()

    # ***************when publisher has verified token*************
    for app in [conf.RTMP, conf.RTMP_HLS]:
        push_retry = 0
        success = False
        while push_retry < 3 and not success:
            push_retry += 1
            multitask = utils.Multitask()
            publisher = utils.Ffmpeg()
            publisher.input(conf.VIDEOS[1])
            publisher.output(utils.get_rtmp_path(app, conf.RESOURCE_ID[1], token), '-f', 'flv')

            subscriber = utils.Ffmpeg()
            subscriber.output(utils.get_rtmp_path(app, conf.RESOURCE_ID[1], token))

            subscriber2 = utils.Ffmpeg()
            subscriber2.output(utils.get_rtmp_path(app, conf.RESOURCE_ID[1], incorrect_token))

            multitask.return_dict[conf.PLAY_VALID] = None
            multitask.return_dict[conf.PLAY_INVALID] = None
            multitask.return_dict[conf.PUSH_VALID] = None

            multitask.add(subscriber.play, conf.PUSH_VALID, conf.PLAY_VALID)
            multitask.add(publisher.push, conf.PUSH_VALID)
            multitask.add(subscriber2.play, conf.PUSH_VALID, conf.PLAY_INVALID)

            multitask.run()

            print(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID],
                  multitask.return_dict[conf.PLAY_INVALID])
            if multitask.return_dict[conf.PUSH_VALID] and multitask.return_dict[conf.PLAY_VALID] and not multitask.return_dict[
                conf.PLAY_INVALID]:
                success = True
        assert success
    print("done")
    sleep(20)
    # ***************when publisher has incorrect token*************
    for app in [conf.RTMP, conf.RTMP_HLS]:
        push_retry = 0
        success = False
        while push_retry < 3 and not success:
            push_retry += 1
            multitask = utils.Multitask()
            publisher = utils.Ffmpeg()
            publisher.input(conf.VIDEOS[1])
            publisher.output(utils.get_rtmp_path(app, conf.RESOURCE_ID[1], incorrect_token), '-f', 'flv')

            subscriber = utils.Ffmpeg()
            subscriber.output(utils.get_rtmp_path(app, conf.RESOURCE_ID[1], token))

            subscriber2 = utils.Ffmpeg()
            subscriber2.output(utils.get_rtmp_path(app, conf.RESOURCE_ID[1], incorrect_token))

            multitask.return_dict[conf.PLAY_VALID] = None
            multitask.return_dict[conf.PLAY_INVALID] = None
            multitask.return_dict[conf.PUSH_VALID] = None

            multitask.add(subscriber.play, conf.PUSH_VALID, conf.PLAY_VALID)
            multitask.add(publisher.push, conf.PUSH_VALID)
            multitask.add(subscriber2.play, conf.PUSH_VALID, conf.PLAY_INVALID)

            multitask.run()

            print(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID],
                  multitask.return_dict[conf.PLAY_INVALID])
            if not multitask.return_dict[conf.PUSH_VALID] and not multitask.return_dict[conf.PLAY_VALID] and not \
            multitask.return_dict[conf.PLAY_INVALID]:
                success = True
        assert success

    print("Token test passed!", file=sys.stderr)


def test_id(token):
    incorrect_id = utils.generate_random_chars()

    # ***************when publisher has verified id*************
    for app in [conf.RTMP, conf.RTMP_HLS]:
        push_retry = 0
        success = False
        while push_retry < 3 and not success:
            push_retry += 1
            multitask = utils.Multitask()
            publisher = utils.Ffmpeg()
            publisher.input(conf.VIDEOS[1])
            publisher.output(utils.get_rtmp_path(app, conf.RESOURCE_ID[1], token), '-f', 'flv')

            subscriber = utils.Ffmpeg()
            subscriber.output(utils.get_rtmp_path(app, conf.RESOURCE_ID[1], token))

            subscriber2 = utils.Ffmpeg()
            subscriber2.output(utils.get_rtmp_path(app, incorrect_id, token))

            multitask.return_dict[conf.PLAY_VALID] = None
            multitask.return_dict[conf.PLAY_INVALID] = None
            multitask.return_dict[conf.PUSH_VALID] = None

            multitask.add(subscriber.play, conf.PUSH_VALID, conf.PLAY_VALID)
            multitask.add(publisher.push, conf.PUSH_VALID)
            multitask.add(subscriber2.play, conf.PUSH_VALID, conf.PLAY_INVALID)

            multitask.run()

            print(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID],
                  multitask.return_dict[conf.PLAY_INVALID])
            if multitask.return_dict[conf.PUSH_VALID] and multitask.return_dict[conf.PLAY_VALID] and not \
            multitask.return_dict[
                conf.PLAY_INVALID]:
                success = True
        assert success
    print("done")
    sleep(20)
    # ***************when publisher has incorrect id*************
    for app in [conf.RTMP, conf.RTMP_HLS]:
        push_retry = 0
        success = False
        while push_retry < 3 and not success:
            push_retry += 1
            multitask = utils.Multitask()
            publisher = utils.Ffmpeg()
            publisher.input(conf.VIDEOS[1])
            publisher.output(utils.get_rtmp_path(app, incorrect_id, token), '-f', 'flv')

            subscriber = utils.Ffmpeg()
            subscriber.output(utils.get_rtmp_path(app, conf.RESOURCE_ID[1], token))

            subscriber2 = utils.Ffmpeg()
            subscriber2.output(utils.get_rtmp_path(app, incorrect_id, token))

            multitask.return_dict[conf.PLAY_VALID] = None
            multitask.return_dict[conf.PLAY_INVALID] = None
            multitask.return_dict[conf.PUSH_VALID] = None

            multitask.add(subscriber.play, conf.PUSH_VALID, conf.PLAY_VALID)
            multitask.add(publisher.push, conf.PUSH_VALID)
            multitask.add(subscriber2.play, conf.PUSH_VALID, conf.PLAY_INVALID)

            multitask.run()

            print(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID],
                  multitask.return_dict[conf.PLAY_INVALID])
            if not multitask.return_dict[conf.PUSH_VALID] and not multitask.return_dict[conf.PLAY_VALID] and not \
                    multitask.return_dict[conf.PLAY_INVALID]:
                success = True
        assert success

    print("Id test passed!", file=sys.stderr)


def test_hd_video(token):
    # TODO: Check resolution, size, duration etc
    for app in [conf.RTMP, conf.RTMP_HLS]:
        push_retry = 0
        success = False
        while push_retry < 3 and not success:
            push_retry += 1
            multitask = utils.Multitask()
            publisher = utils.Ffmpeg()
            publisher.input(conf.VIDEOS["HD"])
            publisher.output(utils.get_rtmp_path(app, conf.RESOURCE_ID[1], token), '-f', 'flv')

            subscriber = utils.Ffmpeg()
            subscriber.output(utils.get_rtmp_path(app, conf.RESOURCE_ID[1], token))

            multitask.return_dict[conf.PLAY_VALID] = None
            multitask.return_dict[conf.PUSH_VALID] = None

            multitask.add(subscriber.dimension, conf.PUSH_VALID, conf.PLAY_VALID)
            multitask.add(publisher.push, conf.PUSH_VALID)

            multitask.run()

            print(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID])
            if multitask.return_dict[conf.PUSH_VALID] and multitask.return_dict[conf.PLAY_VALID]:
                cap = cv2.VideoCapture(conf.VIDEOS["HD"])
                if cap.isOpened():
                    original_dimensions = ( cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    print(multitask.return_dict[conf.PLAY_VALID],original_dimensions)
                    if original_dimensions == multitask.return_dict[conf.PLAY_VALID]:
                        print("Hii")
                        success = True
        assert success

    print("Hd test passed!", file=sys.stderr)


def test_load(token):
    for app in [conf.RTMP, conf.RTMP_HLS]:
        for res_id in conf.RESOURCE_ID.values():
            push_retry = 0
            success = False
            while push_retry < 3 and not success:
                push_retry += 1
                multitask = utils.Multitask()
                publisher = utils.Ffmpeg()
                publisher.input(conf.VIDEOS[1])
                publisher.output(utils.get_rtmp_path(app, res_id, token), '-f', 'flv')

                subscriber = utils.Ffmpeg()
                subscriber.output(utils.get_rtmp_path(app, res_id, token))

                multitask.return_dict[conf.PLAY_VALID] = None
                multitask.return_dict[conf.PUSH_VALID] = None

                multitask.add(subscriber.play, conf.PUSH_VALID, conf.PLAY_VALID)
                multitask.add(publisher.push, conf.PUSH_VALID)

                multitask.run()

                print(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID])
                if multitask.return_dict[conf.PUSH_VALID] and multitask.return_dict[conf.PLAY_VALID]:
                    success = True
            assert success

    print('Load test passed!', file=sys.stderr)


def test_hls(token):

    publisher = utils.Ffmpeg()
    publisher.input(conf.VIDEOS[1])
    publisher.output(utils.get_rtmp_path(conf.RTMP_HLS, conf.RESOURCE_ID[1], token), 'f', 'flv')
    publisher.push({},conf.PUSH_VALID, 20)

    # TODO: Find a way to remove this
    sleep(20)
    response = requests.get('https://localhost:3002/rtmp+hls/' + conf.RESOURCE_ID[1] + '/index.m3u8',
                            cookies={'token': token}, verify=False)
    assert (response.status_code == 200)
    print('HLS test passed!', file=sys.stderr)


def test_live_stream(token):

    multitask = utils.Multitask()

    publisher = utils.Ffmpeg()
    publisher.input(conf.LIVE_STREAM)
    publisher.output(utils.get_rtmp_path(conf.RTMP, conf.RESOURCE_ID[1], token), 'f', 'flv')

    subscriber = utils.Ffmpeg()
    subscriber.input(utils.get_rtmp_path(conf.RTMP, conf.RESOURCE_ID[1], token))

    multitask.add(publisher.push, conf.PUSH_VALID, 100)
    multitask.add(subscriber.get_frame_rate, conf.FRAME_RATE)
    multitask.run()
    print(multitask.return_dict)
    assert( multitask.return_dict['frame_rate'] > 0)

    print("Live Stream Test passed!")

