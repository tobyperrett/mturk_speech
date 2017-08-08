import os
import subprocess
from glob import glob
import re

import config



def sub_compare(s):
    r = re.search('([0-9])+', s)
    return int(r.group(0))

sub_wc = os.path.join(config.youtube_download_dir, "*.sbv")
sub_list = glob(sub_wc)
sub_list.sort(key=lambda l: sub_compare(l))
# print sub_list

sub_numbers = [sub_compare(s) for s in sub_list]


for PID, cap_start in zip(config.PIDs, config.caption_starts):
    vid_wc = os.path.join(PID, config.narrations_subfolder, "*.mp4")
    vid_file_list = glob(vid_wc)
    vid_file_list.sort()

    cap_start_idx = sub_numbers.index(cap_start)

    for i in range(0, len(vid_file_list)):
        old_sub_name = sub_list[i+cap_start_idx]
        cur_vid = vid_file_list[i]
        new_sub_name = os.path.join(config.youtube_output_dir, os.path.split(cur_vid)[1][0:6] + ".sbv")

        print old_sub_name, new_sub_name

        cmd = ["cp", old_sub_name, new_sub_name]

        subprocess.call(cmd)
