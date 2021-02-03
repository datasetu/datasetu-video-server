import os, signal, string, random, test_config as cnf
from moviepy.editor import VideoFileClip

def get_record_length(filename):
    result = VideoFileClip(filename).duration
    return result


def inCloseWrite(event):
    src = event.pathname
    if "%252F" not in src:
        return

    assert (len(src) > 0)
    assert (get_record_length(src) == get_record_length(cnf.VIDEOS[1]))
    print("Recording test passed!")
    os.kill(os.getpid(), signal.SIGINT)

def generate_random_chars(n=32, letters=True, digits=True, special_chars=True):
    generate = ''
    if letters:
        generate+=string.ascii_letters
    if digits:
        generate+=string.digits
    if special_chars:
        generate+=string.punctuation

    return ''.join([random.choice(generate) for _ in range(n)])

def get_rtmp_path(type, id, token):
    return "rtmps://localhost:1935/" + type + "/" + id + "?token=" + token