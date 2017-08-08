from glob import glob
import os
import shutil
import subprocess
import re
import random

import config

def generate_csvs():

    # remove all current csvs
    test=os.listdir(config.mturk_input_dir)
    for item in test:
        if item.endswith(".csv"):
            os.remove(os.path.join(config.mturk_input_dir, item))


    gt_ids = []
    if config.ignore_gt_annotations == True:
        gt_wildcard = os.path.join(config.ground_truth_dir, "*")
        for f_path in glob(gt_wildcard):
            out_fn = os.path.split(f_path)[-1][0:6]
            gt_ids.append(out_fn) 


    gt_files = []
    annotate_files = []

    wildcard = os.path.join(config.mturk_input_dir, "*.wav")
    for dir_fn in glob(wildcard):
        # print dir_fn
        fn = os.path.split(dir_fn)[-1].replace(' ', '%20')
        # print fn
        seq_id = os.path.splitext(fn)[0][0:-3]
        # print seq_id

        server_fn = config.server_address + fn

        # print server_fn

        if seq_id in gt_ids:
            gt_files.append(server_fn)
        else:
            annotate_files.append(server_fn)

    random.shuffle(annotate_files)



    csv_idx = 0
    while len(annotate_files) != 0:
        seq_count = 0
        csv_fn = '{:03d}.csv'.format(csv_idx)
        csv_dir_fn = os.path.join(config.mturk_input_dir, csv_fn)
        with open(csv_dir_fn, 'w') as f:
            f.write(config.csv_first_line + "\n")
            while seq_count < config.max_seqs_per_csv and len(annotate_files) != 0:
                f.write(annotate_files.pop() + "\n")
                seq_count += 1
        csv_idx += 1

