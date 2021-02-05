import subprocess, sys, test_config as cnf, requests
from time import sleep
import ffmpeg
import cv2
import pyinotify
import util
from ffpyplayer.player import MediaPlayer


def callback(ev):
    print(ev._watch_manager._wmd[1])
    # util.inCloseWrite()
    return True


def test_record_length(token):
    ffmpeg \
        .input(cnf.VIDEOS[1]) \
        .output(util.get_rtmp_path(cnf.RTMP_HLS, cnf.RESOURCE_ID[1], token), format='flv') \
        .run_async(
        pipe_stdin=True,
        pipe_stdout=True,
        pipe_stderr=True)
    src_path = cnf.RECORD_SRC_DIR
    wm = pyinotify.WatchManager()
    wm.add_watch(src_path, pyinotify.IN_CLOSE_WRITE, util.inCloseWrite)
    notifier = pyinotify.Notifier(wm)
    notifier.loop()


def test_token(token):
    result = []
    incorrect_token = util.generate_random_chars()
    # ************when publisher has verified token****************
    for type in [cnf.RTMP_HLS, cnf.RTMP]:
        # c = cv2.VideoCapture(cnf.VIDEOS[1])
        rtmp_path = util.get_rtmp_path(type, cnf.RESOURCE_ID[1], token)

        result.append(
            subprocess.Popen(['ffmpeg', '-i', cnf.VIDEOS[1], '-f', 'flv',rtmp_path],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # ffmpeg\
            #     .input('-')\
            #     .output(rtmp_path, format='flv')\
            #     .run_async(pipe_stdout=True,pipe_stderr=True, pipe_stdin=True)
        )
        # while(c.isOpened()):
        #     success, frame = c.read()
        #     if success:
        #         if cv2.waitKey(1) & 0xFF == ord('q'):
        #             break
        #         result[len(result)-1].stdin.write(frame.tostring())
        # c.release()
        # ***************when subscriber has verified token*************
        # cap = cv2.VideoCapture(rtmp_path)
        # counter = 0
        # while (not cap.isOpened()):
        #     cap = cv2.VideoCapture(rtmp_path)
        #     counter += 1
        #     print('Waiting', counter)
        #     sleep(1)
        cap = cv2.VideoCapture(rtmp_path)
        #     if(not cap.isOpened()):
        #         sleep(0.1)
        # result.pop()
        # print('retrying')
        assert (cap.isOpened())
        # TODO: Do not try to play the videos. It's not a practical approach for large loads. Instead capture the frames and store them in a file for processing
        # player  = vlc.MediaPlayer(util.get_rtmp_path(type, cnf.RESOURCE_ID[1], token+'qq'))
        # player.play()
        # player = MediaPlayer(util.get_rtmp_path(type, cnf.RESOURCE_ID[1], token))
        # val = ''
        # while(val != 'eof'):
        #     frame, val = player.get_frame()
        #     if val != 'eof' and frame is not None:
        #         img, t =frame
        #         print(frame)
        # ***************when subscriber has incorrect token*************
        cap = cv2.VideoCapture(util.get_rtmp_path(type, cnf.RESOURCE_ID[1], incorrect_token))
        assert (not cap.isOpened())

    for i in result:
        assert ('error' not in i.communicate()[1].decode('UTF-8'))

    result = []

    # ***************when publisher has incorrect token*************
    for type in [cnf.RTMP_HLS, cnf.RTMP]:
        result.append(
            ffmpeg \
                .input(cnf.VIDEOS[2]) \
                .output(util.get_rtmp_path(type, cnf.RESOURCE_ID[2], incorrect_token), format='flv') \
                .run_async(pipe_stdout=True, pipe_stderr=True)
        )

        # ***************when subscriber has verified token*************
        cap = cv2.VideoCapture(util.get_rtmp_path(type, cnf.RESOURCE_ID[2], token))
        assert (not cap.isOpened())

        # ***************when subscriber has incorrect token*************
        cap = cv2.VideoCapture(util.get_rtmp_path(type, cnf.RESOURCE_ID[2], incorrect_token))
        assert (not cap.isOpened())

    for i in result:
        assert ('error' in i.communicate()[1].decode('UTF-8'))

    print("Token test passed!", file=sys.stderr)


def test_id(token):
    result = []
    incorrect_id = util.generate_random_chars()

    # ***************when publisher has verified id*************
    for type in [cnf.RTMP_HLS, cnf.RTMP]:
        rtmp_path = util.get_rtmp_path(type, cnf.RESOURCE_ID[1], token)

        result.append(
            ffmpeg \
                .input(cnf.VIDEOS[1]) \
                .output(rtmp_path, format='flv') \
                .run_async(pipe_stdout=True, pipe_stderr=True)
        )

        # ***************when subscriber has verified id*************
        cap = cv2.VideoCapture(rtmp_path)
        counter = 0
        while (not cap.isOpened()):
            cap = cv2.VideoCapture(rtmp_path)
            counter += 1
            print('Waiting', counter)
            sleep(1)
        # cap = cv2.VideoCapture(rtmp_path)
        assert (cap.isOpened())

        # ***************when subscriber has incorrect id*************
        cap = cv2.VideoCapture(util.get_rtmp_path(type, incorrect_id, token))
        assert (not cap.isOpened())

    for i in result:
        assert ('error' not in i.communicate()[1].decode('UTF-8'))

    result = []

    # ***************when publisher has verified id*************
    for type in [cnf.RTMP_HLS, cnf.RTMP]:
        result.append(
            ffmpeg \
                .input(cnf.VIDEOS[2]) \
                .output(util.get_rtmp_path(type, incorrect_id, token), format='flv') \
                .run_async(pipe_stdout=True, pipe_stderr=True,pipe_stdin = True)
        )

        # ***************when subscriber has verified id*************
        cap = cv2.VideoCapture(util.get_rtmp_path(type, cnf.RESOURCE_ID[2], token))
        assert (not cap.isOpened())

        # ***************when subscriber has incorrect id*************
        cap = cv2.VideoCapture(util.get_rtmp_path(type, incorrect_id, token))
        assert (not cap.isOpened())

    for i in result:
        assert ('error' in i.communicate()[1].decode('UTF-8'))

    print("Id test passed!", file=sys.stderr)


def test_hd_video(token):
    # TODO: Check resolution, size, duration etc

    result = ffmpeg \
        .input(cnf.VIDEOS["HD"]) \
        .output(util.get_rtmp_path(cnf.RTMP_HLS, cnf.RESOURCE_ID[3], token), format='flv') \
        .run_async(
        pipe_stdin=True,
        pipe_stdout=True,
        pipe_stderr=True)

    assert ('error' not in result.decode('UTF-8'))

    print("hd test passed!", file=sys.stderr)


def test_load(token):
    result = []
    cap = []
    for i in range(1, 4):

        result.append(
            ffmpeg
                .input(cnf.VIDEOS[i if (i < 3) else 'HD'], re=True)
                .output(util.get_rtmp_path(cnf.RTMP, cnf.RESOURCE_ID[i], token), format='flv')
                .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
        )

        for rep in range(1, 4):
            cap.append(cv2.VideoCapture(util.get_rtmp_path(cnf.RTMP, cnf.RESOURCE_ID[rep], token)))

    for i in cap:
        assert (i.isOpened())

    frames = [None] * len(cap)
    ret = [None] * len(cap)

    while True:

        for i, c in enumerate(cap):
            if c is not None:
                ret[i], frames[i] = c.read()

        for i, f in enumerate(frames):
            if ret[i] is True:
                cv2.imshow(str(i), f)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for c in cap:
        if c is not None:
            c.release()

    cv2.destroyAllWindows()

    for i in result:
        print(i)
        assert ('error' in i.communicate().decode('UTF-8'))

    print('load test passed!', file=sys.stderr)


def test_hls(token):
    subprocess.Popen(['ffmpeg', '-i', cnf.video[0], '-f', 'flv',
                      "rtmps://localhost:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # TODO: Find a way to remove this
    sleep(60)
    response = requests.get('https://localhost:3002/rtmp+hls/' + cnf.ids[0] + '/index.m3u8',
                            cookies={'token': token}, verify=False)
    assert (response.status_code == 200)
    print('HLS test passed!', file=sys.stderr)


def test_live_stream(token):
    rtmp = util.get_rtmp_path(cnf.RTMP, cnf.RESOURCE_ID[1], token)
    # Read video and get attributes
    cap = cv2.VideoCapture(0)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    sizeStr = str(size[0]) + 'x' + str(size[1])
    command = ['ffmpeg',
               '-y', '-an',
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-pix_fmt', 'bgr24',
               '-s', sizeStr,
               '-r', '25',
               '-i', '-',
               '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p',
               '-preset', 'ultrafast',
               '-f', 'flv',
               rtmp]
    pipe = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE
                            )
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            pipe.stdin.write(frame.tostring())
    cap.release()
