import subprocess,sys
video = ['Asha _ ARTPARK _ Bengaluru Tech Summit 2020-wKWldDnCZQ0.webm','Talk by Prof  Bharadwaj Amrutur on AI & Robotics Technologies Park ARTPark   a new IISc initiative-QXOXIMgHgZ0.mkv']


ffmpeg_out=subprocess.Popen(['ffmpeg','-i', video[1],'-f', 'flv', "rtmps://video.datasetu.org:1935/rtmp+hls/"+id[0]+"?token=x"+token],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
ffmpeg_stdout,ffmpeg_stderr = ffmpeg_out.communicate()
print(ffmpeg_stdout,ffmpeg_stderr,file=sys.stderr)

ffplay_out = subprocess.Popen(['ffplay', '-i', "rtmps://video.datasetu.org:1935/rtmp+hls/"+id[0]+"?token="+token],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
ffplay_stdout,ffplay_stderr = ffplay_out.communicate()
print(ffplay_stdout,ffplay_stderr,file=sys.stderr)
