#!/usr/bin/env python3

import sys, config as conf,logging
import pyinotify
import utils


def test_record_length(token):
    logging.info("In Record Test")
    multitask = utils.Multitask()

    src_path = conf.RECORD_SRC_DIR
    wm = pyinotify.WatchManager()
    wm.add_watch(src_path, pyinotify.IN_CLOSE_WRITE, utils.inCloseWrite)
    notifier = pyinotify.Notifier(wm)

    publisher = utils.Ffmpeg()
    publisher.input(conf.VIDEOS["countdown"])
    publisher.output(utils.get_rtmp_path(conf.RTMP_HLS, conf.RESOURCE_ID["test-resource-1"], token), '-f', 'flv')

    multitask.add(notifier.loop)
    multitask.add(publisher.push, conf.PUSH_VALID)
    logging.info("Initialising notifier and video stream")
    multitask.run()


def test_token(token):
    logging.info("In token-related tests")
    incorrect_token = utils.generate_random_chars()

    # ***************when publisher has valid token*************

    logging.info("When video is published with a valid token")

    for app in [conf.RTMP, conf.RTMP_HLS]:
        push_retry = 0
        success = False
        while push_retry < 5 and not success:

            logging.info("Stream attempt %d", push_retry + 1)

            push_retry += 1

            multitask = utils.Multitask()
            publisher = utils.Ffmpeg()
            publisher.input(conf.VIDEOS["countdown"])
            publisher.output(utils.get_rtmp_path(app, conf.RESOURCE_ID["test-resource-1"], token), '-f', 'flv')

            logging.info("When subscribed with a valid token")
            subscriber = utils.Ffmpeg()
            subscriber.output(utils.get_rtmp_path(app, conf.RESOURCE_ID["test-resource-1"], token))

            logging.info("When subscribed with an invalid token")
            subscriber2 = utils.Ffmpeg()
            subscriber2.output(utils.get_rtmp_path(app, conf.RESOURCE_ID["test-resource-1"], incorrect_token))

            multitask.return_dict[conf.PLAY_VALID] = None
            multitask.return_dict[conf.PLAY_INVALID] = None
            multitask.return_dict[conf.PUSH_VALID] = None

            multitask.add(subscriber.play, conf.PUSH_VALID, conf.PLAY_VALID)
            multitask.add(publisher.push, conf.PUSH_VALID)
            multitask.add(subscriber2.play, conf.PUSH_VALID, conf.PLAY_INVALID)

            multitask.run()

            logging.debug(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID],
                          multitask.return_dict[conf.PLAY_INVALID])
            if (multitask.return_dict[conf.PUSH_VALID] and multitask.return_dict[conf.PLAY_VALID]
                    and not multitask.return_dict[conf.PLAY_INVALID]):
                success = True
        logging.info("%s publish with valid token has passed!", app)
        assert success

    # ***************when publisher has incorrect token*************

    logging.info("When video is published with an invalid token")

    for app in [conf.RTMP, conf.RTMP_HLS]:
        push_retry = 0
        success = False
        while push_retry < 5 and not success:

            logging.info("Stream attempt %d", push_retry + 1)

            push_retry += 1
            multitask = utils.Multitask()
            publisher = utils.Ffmpeg()
            publisher.input(conf.VIDEOS["countdown"])
            publisher.output(utils.get_rtmp_path(app, conf.RESOURCE_ID["test-resource-1"], incorrect_token), '-f', 'flv')

            logging.info("When subscribed with a valid token")
            subscriber = utils.Ffmpeg()
            subscriber.output(utils.get_rtmp_path(app, conf.RESOURCE_ID["test-resource-1"], token))

            logging.info("When subscribed with an invalid token")
            subscriber2 = utils.Ffmpeg()
            subscriber2.output(utils.get_rtmp_path(app, conf.RESOURCE_ID["test-resource-1"], incorrect_token))

            multitask.return_dict[conf.PLAY_VALID] = None
            multitask.return_dict[conf.PLAY_INVALID] = None
            multitask.return_dict[conf.PUSH_VALID] = None

            multitask.add(subscriber.play, conf.PUSH_VALID, conf.PLAY_VALID)
            multitask.add(publisher.push, conf.PUSH_VALID)
            multitask.add(subscriber2.play, conf.PUSH_VALID, conf.PLAY_INVALID)

            multitask.run()

            logging.debug(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID],
                          multitask.return_dict[conf.PLAY_INVALID])

            if (not multitask.return_dict[conf.PUSH_VALID] and not multitask.return_dict[conf.PLAY_VALID]
                    and not multitask.return_dict[conf.PLAY_INVALID]):
                success = True
        assert success
        logging.info("%s publish with an invalid token has passed!", app)

    logging.info("All access token related tests have passed!")


def test_id(token):
    logging.info("In resource-id tests")
    incorrect_id = utils.generate_random_chars()

    # ***************when publisher has a valid resource-id*************

    logging.info("When video is published with a valid resource-id")

    for app in [conf.RTMP, conf.RTMP_HLS]:
        push_retry = 0
        success = False
        while push_retry < 5 and not success:

            logging.info("Stream attempt: %d", push_retry + 1)

            push_retry += 1
            multitask = utils.Multitask()
            publisher = utils.Ffmpeg()
            publisher.input(conf.VIDEOS["countdown"])
            publisher.output(utils.get_rtmp_path(app, conf.RESOURCE_ID["test-resource-1"], token), '-f', 'flv')

            logging.info("When subscribed with a valid resource-id")
            subscriber = utils.Ffmpeg()
            subscriber.output(utils.get_rtmp_path(app, conf.RESOURCE_ID["test-resource-1"], token))

            logging.info("When subscribed with an invalid resource-id")
            subscriber2 = utils.Ffmpeg()
            subscriber2.output(utils.get_rtmp_path(app, incorrect_id, token))

            multitask.return_dict[conf.PLAY_VALID] = None
            multitask.return_dict[conf.PLAY_INVALID] = None
            multitask.return_dict[conf.PUSH_VALID] = None

            multitask.add(subscriber.play, conf.PUSH_VALID, conf.PLAY_VALID)
            multitask.add(publisher.push, conf.PUSH_VALID)
            multitask.add(subscriber2.play, conf.PUSH_VALID, conf.PLAY_INVALID)

            multitask.run()

            logging.debug(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID],
                          multitask.return_dict[conf.PLAY_INVALID])

            if (multitask.return_dict[conf.PUSH_VALID] and multitask.return_dict[conf.PLAY_VALID]
                    and not multitask.return_dict[conf.PLAY_INVALID]):
                success = True
        assert success

        logging.info("%s publish with a valid resource-id has passed!", app)

    # ***************when publisher has invalid id*************

    logging.info("When video is published with an invalid resource-id")

    for app in [conf.RTMP, conf.RTMP_HLS]:
        push_retry = 0
        success = False
        while push_retry < 5 and not success:

            logging.info("Stream attempt: %d", push_retry + 1)

            push_retry += 1
            multitask = utils.Multitask()
            publisher = utils.Ffmpeg()
            publisher.input(conf.VIDEOS["countdown"])
            publisher.output(utils.get_rtmp_path(app, incorrect_id, token), '-f', 'flv')

            logging.info("When subscribed with an valid resource-id")
            subscriber = utils.Ffmpeg()
            subscriber.output(utils.get_rtmp_path(app, conf.RESOURCE_ID["test-resource-1"], token))

            logging.info("When subscribed with invalid resource-id")
            subscriber2 = utils.Ffmpeg()
            subscriber2.output(utils.get_rtmp_path(app, incorrect_id, token))

            multitask.return_dict[conf.PLAY_VALID] = None
            multitask.return_dict[conf.PLAY_INVALID] = None
            multitask.return_dict[conf.PUSH_VALID] = None

            multitask.add(subscriber.play, conf.PUSH_VALID, conf.PLAY_VALID)
            multitask.add(publisher.push, conf.PUSH_VALID)
            multitask.add(subscriber2.play, conf.PUSH_VALID, conf.PLAY_INVALID)

            multitask.run()

            logging.debug(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID],
                          multitask.return_dict[conf.PLAY_INVALID])

            if (not multitask.return_dict[conf.PUSH_VALID] and not multitask.return_dict[conf.PLAY_VALID]
                    and not multitask.return_dict[conf.PLAY_INVALID]):
                success = True
        assert success

        logging.info("%s publish with a valid resource-id has passed!", app)

    logging.info("All resource-ids related tests have passed!")


def test_hd_video(token):
    # TODO: Check resolution, size, duration etc

    logging.info("In HD video test")
    for app in [conf.RTMP, conf.RTMP_HLS]:
        push_retry = 0
        success = False
        while push_retry < 5 and not success:
            logging.info("Stream attempt: %d", push_retry+1)
            push_retry += 1
            multitask = utils.Multitask()
            publisher = utils.Ffmpeg()
            publisher.input(conf.VIDEOS["HD"])
            publisher.output(utils.get_rtmp_path(app, conf.RESOURCE_ID["test-resource-1"], token), '-f', 'flv')

            logging.info("When subscribed with an valid resource-id")
            subscriber = utils.Ffmpeg()
            subscriber.output(utils.get_rtmp_path(app, conf.RESOURCE_ID["test-resource-1"], token))

            multitask.return_dict[conf.PLAY_VALID] = None
            multitask.return_dict[conf.PUSH_VALID] = None

            multitask.add(subscriber.get_dimensions, conf.PUSH_VALID, conf.PLAY_VALID)
            multitask.add(publisher.push, conf.PUSH_VALID)

            multitask.run()

            logging.debug(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID])

            if multitask.return_dict[conf.PUSH_VALID] and multitask.return_dict[conf.PLAY_VALID]:
                if utils.validate_dimension(conf.VIDEOS["HD"],multitask.return_dict[conf.PLAY_VALID]):
                    success = True
        assert success

        logging.info("HD video test with %s has passed", app)

    logging.info("All HD video tests have passed!")


def test_load(token):

    logging.info("In load tests")
    for app in [conf.RTMP, conf.RTMP_HLS]:
        for res_id in conf.RESOURCE_ID.values():
            logging.debug("Trying with %s", res_id)
            push_retry = 0
            success = False
            while push_retry < 5 and not success:

                logging.info("Stream attempt %d", push_retry + 1)

                push_retry += 1
                multitask = utils.Multitask()
                publisher = utils.Ffmpeg()
                publisher.input(conf.VIDEOS["countdown"])
                publisher.output(utils.get_rtmp_path(app, res_id, token), '-f', 'flv')

                logging.info("subscribing with %s", res_id)
                subscriber = utils.Ffmpeg()
                subscriber.output(utils.get_rtmp_path(app, res_id, token))

                multitask.return_dict[conf.PLAY_VALID] = None
                multitask.return_dict[conf.PUSH_VALID] = None

                multitask.add(subscriber.play, conf.PUSH_VALID, conf.PLAY_VALID)
                multitask.add(publisher.push, conf.PUSH_VALID)

                multitask.run()

                logging.debug(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID])

                if multitask.return_dict[conf.PUSH_VALID] and multitask.return_dict[conf.PLAY_VALID]:
                    success = True

            assert success
            logging.info("Passed with app %s and id %s", [app], [res_id])

    logging.info('All load tests have passed!')


def test_hls(token):
    success = False

    multitask = utils.Multitask()
    publisher = utils.Ffmpeg()

    logging.info("Published with asha video")
    publisher.input(conf.VIDEOS["countdown"])
    publisher.filter('-c:v', 'libx264', '-preset', 'veryfast', '-maxrate', '3000k', '-bufsize', '6000k', '-pix_fmt',
                     'yuv420p', '-g', '50', '-c:a', 'aac', '-b:a', '160k', '-ac', '2', '-ar', '44100')
    publisher.output(utils.get_rtmp_path(conf.RTMP_HLS, conf.RESOURCE_ID["test-resource-1"], token), '-f', 'flv')

    logging.info("Subscribing with HLS")
    subscriber = utils.Ffmpeg()
    subscriber.output(None,conf.RESOURCE_ID["test-resource-1"],token)

    multitask.return_dict[conf.PUSH_VALID] = None
    multitask.return_dict[conf.PLAY_VALID] = None

    multitask.add(subscriber.hls, conf.PUSH_VALID, conf.PLAY_VALID)
    multitask.add(publisher.push, conf.PUSH_VALID)

    multitask.run()


    logging.debug(multitask.return_dict[conf.PLAY_VALID], multitask.return_dict[conf.PUSH_VALID])

    if (multitask.return_dict[conf.PUSH_VALID] and multitask.return_dict[conf.PLAY_VALID] == 200):
        success = True

    assert success

    print('All HLS tests have passed!', file=sys.stderr)


def test_live_stream(token):
    multitask = utils.Multitask()

    publisher = utils.Ffmpeg()
    publisher.input(conf.LIVE_STREAM)
    publisher.output(utils.get_rtmp_path(conf.RTMP, conf.RESOURCE_ID["test-resource-1"], token), 'f', 'flv')

    subscriber = utils.Ffmpeg()
    subscriber.input(utils.get_rtmp_path(conf.RTMP, conf.RESOURCE_ID["test-resource-1"], token))

    multitask.add(publisher.push, conf.PUSH_VALID, 100)
    # multitask.add(subscriber.get_frame_rate, conf.FRAME_RATE)
    multitask.run()
    logging.debug(multitask.return_dict)
    assert (multitask.return_dict['frame_rate'] > 0)

    logging.info("Live Stream Test passed!")
