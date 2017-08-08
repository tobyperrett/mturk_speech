from pydub import AudioSegment
import pydub
from pydub.silence import split_on_silence
from glob import glob
import os
import shutil
import sys
import argparse

import config



def split_single_file(audio_file_name, audio_file_extension, silence_thresh):
    print 'processing: ' + audio_file_name

    new_dir = os.path.splitext(audio_file_name)[0].split('/')[0:-1]
    
    
    clip_name = os.path.splitext(os.path.split(audio_file_name)[1])[0]
    clip_name = clip_name[0:6]

    new_dir.append(clip_name)
    new_dir = os.path.join(*new_dir)

    shutil.rmtree(new_dir, ignore_errors=True)
    os.makedirs(new_dir)

    audio = AudioSegment.from_file(audio_file_name, audio_file_extension)
    audio = pydub.effects.normalize(audio)

    print "length original: " + str(audio.duration_seconds) + "s"
    chunks = split_on_silence(audio, config.min_silence_len, silence_thresh, keep_silence = config.chunk_separation)
    print "found " + str(len(chunks)) + " chunks" 
    silent_chunk = AudioSegment.silent(duration = 0)

    merged = AudioSegment.empty()
    save_chunk = AudioSegment.empty()
    save_idx = 0
    for i, chunk in enumerate(chunks):
        merged = merged + chunk + silent_chunk
        save_chunk = save_chunk + chunk + silent_chunk
        
        if save_chunk.duration_seconds > config.save_seq_length_secs:
            # chunk_fn = clip_name + '_' + str(save_idx) + '.' + config.chunk_extension
            chunk_fn = '{}_{:02d}.{}'.format(clip_name, save_idx, config.chunk_extension)
            out_file = os.path.join(config.mturk_input_dir, chunk_fn)
            # print "saving: " + out_file


            save_chunk.export(out_file, format = config.chunk_extension)
            save_chunk = AudioSegment.empty()
            save_idx += 1

    if save_chunk.duration_seconds > 0:
        chunk_fn = '{}_{:02d}.{}'.format(clip_name, save_idx, config.chunk_extension)
        out_file = os.path.join(config.mturk_input_dir, chunk_fn)
        # print "saving: " + out_file
        save_chunk.export(out_file, format = config.chunk_extension)
        save_chunk = AudioSegment.empty()
        save_idx += 1

            
    
    print "length merged: " + str(merged.duration_seconds) + "s"

    merged_fn = clip_name + '_' + 'short.' + config.chunk_extension
    out_file = os.path.join(new_dir, merged_fn)
    merged.export(out_file, format = config.chunk_extension)

def split_all():
    for person_directory, audio_file_extension, silence_thresh in zip(config.PIDs, config.audio_file_extensions, config.thresholds):
        audio_file_wildcard = person_directory + '/' + config.narrations_subfolder + '/*.' + audio_file_extension 
        for fn in glob(audio_file_wildcard):
            split_single_file(fn, audio_file_extension, silence_thresh)   

def main():
    # print sys.argv

    if len(sys.argv) != 4:
        print "example usage: python split_silence.py P02_04 mp3 -40"
        return

    seq_id = sys.argv[1]
    ext = sys.argv[2]
    person_directory = seq_id[0:3]
    threshold = int(sys.argv[3])

    fn = os.path.join(person_directory, config.narrations_subfolder, seq_id  + "." + ext)

    print "splitting: " + fn + ", with threshold: " + str(threshold)
    print "split output in: " + config.mturk_input_dir
    print "joined output (with silence removed) in: " + os.path.join(person_directory, config.narrations_subfolder, seq_id, "short." + config.chunk_extension)
            
    split_single_file(fn, ext, threshold)   



if __name__ == '__main__':
    main()

