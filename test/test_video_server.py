import subprocess, os, sys, test_config as cnf, requests
import watchdog.events
import watchdog.observers
from moviepy.editor import VideoFileClip
from time import sleep


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, observer):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.flv'],
                                                             ignore_directories=True, case_sensitive=False)
        self.observer = observer

    def get_record_length(self, filename):
        result = VideoFileClip(filename).duration
        return result

    def on_created(self, event):
        src = event.src_path

        if "%252F" not in src:
            return
        assert (len(src) > 0)
        sleep(60)
        assert (self.get_record_length(src) == self.get_record_length(cnf.video[0]))
        print("Recording test passed!", file=sys.stderr)
        self.observer.unschedule_all()
        self.observer.stop()


def test_token(token):
    ffmpeg_out = subprocess.Popen(['ffmpeg', '-i', cnf.video[0], '-f', 'flv',
                                   "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ffmpeg_stdout, ffmpeg_stderr = ffmpeg_out.communicate()
    assert ('error' not in ffmpeg_stderr.decode('UTF-8'))

    ffmpeg_out1 = subprocess.Popen(['ffmpeg', '-i', cnf.video[1], '-f', 'flv',
                                    "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[
                                        1] + "?token=~!@#$%^&*()_+}{[]:|;'\<>?,./`'" + token],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    ffmpeg_stdout, ffmpeg_stderr = ffmpeg_out1.communicate()
    assert ('error' in ffmpeg_stderr.decode('UTF-8'))

    ffmpeg_out = subprocess.Popen(['ffmpeg', '-i', cnf.video[0], '-f', 'flv',
                                   "rtmps://video.datasetu.org:1935/rtmp/" + cnf.ids[0] + "?token=" + token],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ffmpeg_stdout, ffmpeg_stderr = ffmpeg_out.communicate()
    assert ('error' not in ffmpeg_stderr.decode('UTF-8'))

    ffmpeg_out1 = subprocess.Popen(['ffmpeg', '-i', cnf.video[1], '-f', 'flv',
                                    "rtmps://video.datasetu.org:1935/rtmp/" + cnf.ids[
                                        1] + "?token=~!@#$%^&*()_+}{[]:|;'\<>?,./`'" + token],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    ffmpeg_stdout, ffmpeg_stderr = ffmpeg_out1.communicate()
    assert ('error' in ffmpeg_stderr.decode('UTF-8'))

    print("Token test passed!", file=sys.stderr)


def test_id(token):
    ffmpeg_out = subprocess.Popen(['ffmpeg', '-i', cnf.video[0], '-f', 'flv',
                                   "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ffmpeg_stdout, ffmpeg_stderr = ffmpeg_out.communicate()
    assert ('error' not in ffmpeg_stderr.decode('UTF-8'))

    ffmpeg_out1 = subprocess.Popen(['ffmpeg', '-i', cnf.video[1], '-f', 'flv',
                                    "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[
                                        1] + "~!@#$%^&*()_+}{[]:|;'\<>?,./`'?token=" + token],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    ffmpeg_stdout, ffmpeg_stderr = ffmpeg_out1.communicate()
    assert ('error' in ffmpeg_stderr.decode('UTF-8'))

    ffmpeg_out = subprocess.Popen(['ffmpeg', '-i', cnf.video[0], '-f', 'flv',
                                   "rtmps://video.datasetu.org:1935/rtmp/" + cnf.ids[0] + "?token=" + token],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ffmpeg_stdout, ffmpeg_stderr = ffmpeg_out.communicate()
    assert ('error' not in ffmpeg_stderr.decode('UTF-8'))

    ffmpeg_out1 = subprocess.Popen(['ffmpeg', '-i', cnf.video[1], '-f', 'flv',
                                    "rtmps://video.datasetu.org:1935/rtmp/" + cnf.ids[
                                        1] + "~!@#$%^&*()_+}{[]:|;'\<>?,./`'?token=" + token],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    ffmpeg_stdout, ffmpeg_stderr = ffmpeg_out1.communicate()
    assert ('error' in ffmpeg_stderr.decode('UTF-8'))

    print("Id test passed!", file=sys.stderr)


def test_record_length(token):
    src_path = cnf.RECORD_SRC_DIR
    observer = watchdog.observers.Observer()
    event_handler = Handler(observer)
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    ffmpeg_out = subprocess.Popen(['ffmpeg', '-i', cnf.video[0], '-f', 'flv',
                                   "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ffmpeg_stdout, ffmpeg_stderr = ffmpeg_out.communicate()


def test_hd_video(token):
    ffmpeg_out = subprocess.Popen(['ffmpeg', '-i', cnf.video[2], '-f', 'flv',
                                   "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    ffmpeg_stdout, ffmpeg_stderr = ffmpeg_out.communicate()
    assert ('error' not in ffmpeg_stderr.decode('UTF-8'))
    print("hd test passed!", file=sys.stderr)


def test_load(token):
    subprocess.Popen(['ffmpeg', '-i', cnf.video[0], '-f', 'flv',
                      "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.Popen(['ffmpeg', '-i', cnf.video[1], '-f', 'flv',
                      "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.Popen(['ffmpeg', '-i', cnf.video[2], '-f', 'flv',
                      "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.Popen(
        ['ffplay', '-i', "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.Popen(
        ['ffplay', '-i', "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.Popen(
        ['ffplay', '-i', "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.Popen(
        ['ffplay', '-i', "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[1] + "?token=" + token],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.Popen(
        ['ffplay', '-i', "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[1] + "?token=" + token],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.Popen(
        ['ffplay', '-i', "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[1] + "?token=" + token],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.Popen(
        ['ffplay', '-i', "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[2] + "?token=" + token],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.Popen(
        ['ffplay', '-i', "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[2] + "?token=" + token],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.Popen(
        ['ffplay', '-i', "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[2] + "?token=" + token],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print('load test passed!', file=sys.stderr)


def test_hls(token):
    subprocess.Popen(['ffmpeg', '-i', cnf.video[0], '-f', 'flv',
                      "rtmps://video.datasetu.org:1935/rtmp+hls/" + cnf.ids[0] + "?token=" + token],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    sleep(120)
    response = requests.get('https://video.datasetu.org:3002/rtmp+hls/' + cnf.ids[0] + '/index.m3u8',
                            cookies={'token': token}, verify=False)
    assert (response.status_code == 200)
    print('HLS test passed!', file=sys.stderr)
