import os, subprocess, signal, string, random, test_config as cnf
from moviepy.editor import VideoFileClip
from time import sleep
from multiprocessing import Process, Manager

class Ffmpeg:
    def __init__(self):
        self.input_args = []
        self.output_args = []
        self.global_args = []
        self.result = True

    def input(self, input_file = None, *input_args, **input_kwargs):
        for arg in input_args:
            self.input_args.append('-' + arg)

        for key, value in input_kwargs:
            self.input_args.append('-' + key)
            self.input_args.append(value)

        if input_file == None:
            self.input_args.append('-i')
            self.input_args.append('-')

        elif 'i' not in input_kwargs.keys():
            self.input_args.append('-i')
            self.input_args.append(input_file)
            
    def filter(self, *global_args, **global_kwargs):
        for arg in global_args:
            self.global_args.append('-' + arg)

        for key, value in global_kwargs:
            self.global_args.append('-' + key)
            self.global_args.append(value)
            
    def output(self, output_file, *output_args, **output_kwargs):
        for arg in output_args:
            self.output_args.append('-' + arg)

        for key, value in output_kwargs:
            self.output_args.append('-' + key)
            self.output_args.append(value)

        if 'f' not in output_kwargs.keys():
            self.output_args.append('-f')
        self.output_args.append('flv')

        self.output_args.append(output_file)

    def push(self, return_dict, type = None, timeout = None):
        res = subprocess.Popen(['ffmpeg'] + self.input_args + self.global_args + self.output_args + ['-loglevel','error'], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        if not res.poll() and timeout:
            sleep(timeout)
            res.terminate()
        errors = res.communicate()[1].decode('UTF-8')
        if len(errors) >0:
            self.result = False
        # print(res.returncode)
        res.terminate()

        return_dict[type] = self.result

    def play(self,return_dict, type = None, timeout = None):
        res = subprocess.Popen(['ffplay'] + self.input_args + self.global_args + self.output_args  + ['-loglevel','error'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not res.poll() and timeout:
            sleep(timeout)
            res.terminate()
        errors = res.communicate()[1].decode('UTF-8')
        if len(errors):
            self.result = False
        res.terminate()
        # print(errors, type)
        return_dict[type] = self.result

class Multitask:
    def __init__(self):
        self.return_dict = Manager().dict()
        self.jobs = []

    def add(self, process, type = None, timeout = None):
        if type is None:
            self.jobs.append(Process(target=process))
        else:
            self.jobs.append(Process(target=process, args=(self.return_dict, type, timeout,)))

    def run(self,):
        for process in self.jobs:
            process.start()

        for process in self.jobs:
            process.join()

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