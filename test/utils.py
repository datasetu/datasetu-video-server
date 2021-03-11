import os, subprocess, signal, string, random, config as conf
from moviepy.editor import VideoFileClip
from multiprocessing import Process, Manager
import cv2, logging, ctypes, io , sys, tempfile, requests, time
from contextlib import contextmanager

libc = ctypes.CDLL(None)
c_stderr = ctypes.c_void_p.in_dll(libc, 'stderr')


@contextmanager
def stderr_redirector(stream):
    original_stderr_fd = sys.stderr.fileno()

    def _redirect_stderr(to_fd):
        libc.fflush(c_stderr)
        sys.stderr.close()
        os.dup2(to_fd, original_stderr_fd)
        sys.stderr = io.TextIOWrapper(os.fdopen(original_stderr_fd, 'wb'))

    saved_stderr_fd = os.dup(original_stderr_fd)
    try:
        tfile = tempfile.TemporaryFile(mode='w+b')
        _redirect_stderr(tfile.fileno())
        yield
        _redirect_stderr(saved_stderr_fd)
        tfile.flush()
        tfile.seek(0, io.SEEK_SET)
        stream.write(tfile.read().decode())
    finally:
        tfile.close()
        os.close(saved_stderr_fd)


class Ffmpeg:
    def __init__(self):
        self.input_args = []
        self.output_args = []
        self.global_args = []
        self.result = None

    def input(self, input_file=None, *input_args, **input_kwargs):
        for arg in input_args:
            self.input_args.append(arg)

        for key, value in input_kwargs:
            self.input_args.append(key)
            self.input_args.append(value)

        if input_file is None:
            self.input_args.append('-i')
            self.input_args.append('-')

        if '-i' not in input_args or '-i' not in input_kwargs.keys():
            self.input_args.append('-i')
            self.input_args.append(input_file)

    def filter(self, *global_args, **global_kwargs):
        for arg in global_args:
            self.global_args.append(arg)

        for key, value in global_kwargs:
            self.global_args.append(key)
            self.global_args.append(value)

    def output(self, output_file, *output_args, **output_kwargs):
        for arg in output_args:
            self.output_args.append(arg)

        for key, value in output_kwargs:
            self.output_args.append(key)
            self.output_args.append(value)
        if output_file:
            self.output_args.append(output_file)

    def push(self, return_dict, push_key=None, play_key=None):
        logging.debug("In Push, push_key:", push_key, "play_key:", play_key)
        res = subprocess.Popen(
            ['ffmpeg'] + self.input_args + self.global_args + self.output_args + ['-loglevel', 'error'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        errors = res.communicate()[1].decode('UTF-8')

        if len(errors) > 0:
            self.result = False
        else:
            self.result = True
        return_dict[push_key] = self.result

    def play(self, return_dict, push_key=None, play_key=None):
        logging.debug("In Play, push_key:", push_key, "play_key:", play_key)
        while return_dict[push_key] is None:
            logging.debug("Video is still streaming")
            logging.debug("Value of push", return_dict[push_key])
            f = io.StringIO()
            with stderr_redirector(f):
                cap = cv2.VideoCapture(self.output_args[0])
                if cap.isOpened():
                    logging.debug("OpenCV video capture succeeded")
                    self.result = True
                    logging.debug("Result", self.result)
                    break
                else:
                    self.result = False
            f.close()
        return_dict[play_key] = self.result

    def get_dimensions(self, return_dict, push_key=None, play_key=None):
        logging.debug("In get dimensions, push_key:", push_key, "play_key:", play_key)
        while return_dict[push_key] is None:
            logging.debug("Video is still streaming")
            logging.debug("Value of Push", return_dict[push_key])
            f = io.StringIO()
            with stderr_redirector(f):
                cap = cv2.VideoCapture(self.output_args[0])
                if cap.isOpened():
                    logging.debug("OpenCV video capture succeeded")
                    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    self.result = (width, height)
                    logging.debug("Result", self.result)
                    break
            f.close()
        return_dict[play_key] = self.result

    def hls(self, return_dict, push_key=None, play_key=None):
        logging.debug("In HLS, push_key:", push_key, "play_key:", play_key)
        timeout = 0
        while timeout < 60:
            logging.info("Video Capture Attempt %d", timeout+1)
            logging.debug("Video is still Streaming")
            logging.debug("Value of Push", return_dict[push_key])
            response = requests.get('https://localhost:3002/rtmp+hls/' + self.output_args[0] + '/index.m3u8',
                                    cookies={'token': self.output_args[1]}, verify=False)
            if response.status_code == 200:
                self.result = response.status_code
                break
            time.sleep(1)
            timeout += 1
        return_dict[play_key] = self.result

class Multitask:
    def __init__(self):
        self.return_dict = Manager().dict()
        self.jobs = []

    def add(self, process, push_key=None, play_key=None):
        if not (push_key or play_key):
            self.jobs.append(Process(target=process))
        else:
            logging.debug(push_key, play_key)
            self.jobs.append(Process(target=process, args=(self.return_dict, push_key, play_key,)))

    def run(self, ):
        for process in self.jobs:
            process.start()

        for process in self.jobs:
            process.join()


def get_record_length(filename):
    result = VideoFileClip(filename).duration
    return result


def inCloseWrite(event):
    logging.info("Recording complete event triggered")
    src = event.pathname
    if "%252F" not in src:
        return
    assert (len(src) > 0)
    assert (int(get_record_length(src)) == int(get_record_length(conf.VIDEOS["countdown"])))
    logging.info("Recording test has passed!")
    os.kill(os.getpid(), signal.SIGINT)


def generate_random_chars(n=32, letters=True, digits=True, special_chars=True):
    generate = ''
    if letters:
        generate += string.ascii_letters
    if digits:
        generate += string.digits
    if special_chars:
        generate += string.punctuation

    return ''.join([random.choice(generate) for _ in range(n)])


def get_rtmp_path(type, id, token):
    return "rtmps://localhost:1935/" + type + "/" + id + "?token=" + token


def validate_dimension(original_video, result):
    cap_retry = 0
    success = False
    while cap_retry < 5 and not success:

        logging.info("Video capture attempt %d", cap_retry+1)

        cap_retry += 1
        cap = cv2.VideoCapture(original_video)
        if cap.isOpened():
            original_dimensions = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            logging.debug(result, original_dimensions)
            if original_dimensions == result:
                logging.debug("Dimension Matches")
                success = True
    return success
