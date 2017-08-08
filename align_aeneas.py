import csv
from glob import glob
import os
from aeneas.executetask import ExecuteTask
from aeneas.task import Task


import config


def align_aeneas():


    for PID in config.PIDs:

        audio_wc = os.path.join(PID, config.narrations_subfolder, "*.m4a")
        audio_file_list = glob(audio_wc)

        if len(audio_file_list) == 0:
            audio_wc = os.path.join(PID, config.narrations_subfolder, "*.mp3")
            audio_file_list = glob(audio_wc)


        audio_file_list.sort()


        for a in audio_file_list:
            file_id = os.path.split(a)[1][0:6]
            t = os.path.join(config.aeneas_transcript_dir, file_id + ".txt")
            out_file = os.path.join(config.aeneas_output_dir, file_id + ".sbv")
            print "aligning " + a, t

            if not os.path.isfile(t):
                print t + " not available so will not be processed.  Was it a missed ground truth file?"
                continue

            # create Task object
            config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=sbv"
            task = Task(config_string=config_string)
            task.audio_file_path_absolute = a
            task.text_file_path_absolute = t
            task.sync_map_file_path_absolute = out_file

            # process Task
            ExecuteTask(task).execute()

            # output sync map to file
            task.output_sync_map_file()


