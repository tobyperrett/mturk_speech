from pydub import AudioSegment
import pydub
from pydub.silence import split_on_silence
from glob import glob
import os
import shutil
import subprocess
import re

import config

def getLengthSeconds(filename):
    process = subprocess.Popen(["ffprobe", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    stdout, stderr = process.communicate()
    matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()

    seconds = int(matches['hours'])*60*60 + int(matches['minutes'])*60 + int(float(matches['seconds'])) + 1

    return seconds

def create_video(audio_file_name):
    print 'processing: ' + audio_file_name
    # video_file_name = os.path.splitext(audio_file_name)[0] + '.' + config.video_extension
    # out_fn = os.path.splitext(audio_file_name)[0] + '_youtube.' + config.video_extension

    # print out_fn

    new_dir = os.path.splitext(audio_file_name)[0].split('/')[0:-1]
    clip_name = os.path.splitext(os.path.split(audio_file_name)[1])[0]
    clip_name = clip_name[0:6]+ '_youtube.' + config.video_extension
    new_dir.append(clip_name)

    out_fn = os.path.join(*new_dir)


    length = getLengthSeconds(audio_file_name)


    
    fr_str = '1/' + str(length)
    cmd = ['ffmpeg', '-framerate', fr_str, '-i', config.black_img, '-i', audio_file_name, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-profile:v', 'baseline', '-level', '3.0', '-r', '30', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-strict', 'experimental', '-b:a', '192k', '-shortest', out_fn]
    
    subprocess.call(cmd)

    # cmd = ['ffmpeg', '-i', video_file_name, '-i', audio_file_name, '-map',  '0:0',  '-map',  '1:0',  '-c:v',  'copy',  '-c:a', 'copy', '-shortest', out_fn]
    # ffmpeg -i INPUT.mp4 -i AUDIO.wav -map 0:0 -map 1:0 -c:v copy -c:a aac -b:a 256k -shortest OUTPUT.mp4 

def create_all_videos():
    for person_directory, audio_file_extension in zip(config.PIDs, config.audio_file_extensions):
        audio_file_wildcard = person_directory + '/' + config.narrations_subfolder + '/*.' + audio_file_extension    
        for fn in glob(audio_file_wildcard):
            create_video(fn)   

def main():
    audio_file_wildcard = person_directory + '/' + config.narrations_subfolder + '/*.' + audio_file_extension    
    for fn in glob(audio_file_wildcard):
        create_video(fn) 

if __name__ == '__main__':
    main()

