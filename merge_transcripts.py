import csv
from glob import glob
import os
from shutil import copyfile
import string
import re
import itertools
import enchant

from Levenshtein import distance

import config

spell_check = enchant.Dict("en_UK")

def xstr(s):
    return '' if s is None else str(s)



def inspect_transcripts(t_list, subseq, best_idx_1, best_idx_2, min_dist):
    t_list_lines = []
    bad_words_list = []
    for t in t_list:
        bad_words = []
        words = t.split()
        for word in words:
            if spell_check.check(word) == False:
                print word
                bad_words.append(word)
        bad_words_list.append(set(bad_words))
        t_list_lines.append(t.splitlines())

    os.system('cls' if os.name == 'nt' else 'clear')
    print "{} and {} are closest with a difference of {}.".format(best_idx_1+1, best_idx_2+1, min_dist)

    print ""
    for c1, c2, c3 in itertools.izip_longest(*t_list_lines):
        print "%-50s %-50s %s" % (xstr(c1), xstr(c2), xstr(c3))
    print ""

    print "Potential spelling errors:"
    for c1, c2, c3 in itertools.izip_longest(*bad_words_list):
        print "%-50s %-50s %s" % (xstr(c1), xstr(c2), xstr(c3))
    print ""

    choice = input("Select correct transcription for {} by typing 1,2 or 3. Type 0 if all are wrong to manually correct later.\n".format(subseq))

    return int(choice) - 1

def clean_and_compare_transcripts(t_list, subseq):

    n_transcripts = len(t_list)

    t_list_clean = []

    for t in t_list:

        t = os.linesep.join([s for s in t.splitlines() if s])

        t_clean = ""

        for l in t.splitlines():
            l_clean = l.translate(None, string.punctuation).strip().lower() + "\n"
            l_clean = re.sub(' +', ' ', l_clean)
            t_clean += l_clean

        t_list_clean.append(t_clean)

    min_distance = 10000000
    best_idx_1 = -1
    best_idx_2 = -2
    for idx_1 in range(0, n_transcripts):
        for idx_2 in range(idx_1 + 1, n_transcripts):
            tmp_dist = distance(t_list_clean[idx_1], t_list_clean[idx_2])
            if tmp_dist < min_distance:
                min_distance = tmp_dist
                best_idx_2 = idx_2
                best_idx_1 = idx_1

    # print min_distance
    # print t_list_clean[best_idx_1]
    # print t_list_clean[best_idx_2]

    if min_distance == 0:
        return min_distance, t_list_clean[best_idx_1]

    correct_idx = inspect_transcripts(t_list_clean, subseq, best_idx_1, best_idx_2, min_distance)
    if correct_idx >= 0 and correct_idx <= 2:
        return 0, t_list_clean[correct_idx]


    return -1, t_list_clean[best_idx_1]






def process_transcripts():

    error_exists = False

    wildcard = os.path.join(config.mturk_results_dir, "Batch*.csv")

    column_names = ["HITId","HITTypeId","Title","Description","Keywords","Reward","CreationTime","MaxAssignments","RequesterAnnotation","AssignmentDurationInSeconds","AutoApprovalDelayInSeconds","Expiration","NumberOfSimilarHITs","LifetimeInSeconds","AssignmentId","WorkerId","AssignmentStatus","AcceptTime","SubmitTime","AutoApprovalTime","ApprovalTime","RejectionTime","RequesterFeedback","WorkTimeInSeconds","LifetimeApprovalRate","Last30DaysApprovalRate","Last7DaysApprovalRate","Input.media-link","Answer.TranscriptionTexts","Approve","Reject"]

    whole_seqs = []
    num_parts = []
    transcriptions = {}

    for fn in glob(wildcard):
        with open(fn, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                link =  row["Input.media-link"]
                trans =  row["Answer.TranscriptionTexts"]
                accept_status = row["AssignmentStatus"]

                if accept_status == "Rejected":
                    continue

                sub_seq = os.path.splitext(link.split("/")[-1])[0]

                transcriptions.setdefault(sub_seq, [])
                transcriptions[sub_seq].append(trans)

                seq_id = sub_seq[0:-3]
                subseq_id = int(sub_seq[-2:])
                pid = seq_id[0:3]

                if pid not in config.PIDs:
                    continue

                if seq_id not in whole_seqs:
                    whole_seqs.append(seq_id)
                    num_parts.append(subseq_id)
                else:
                    file_idx = whole_seqs.index(seq_id)
                    if subseq_id > num_parts[file_idx]:
                        num_parts[file_idx] = subseq_id

    for s, p in zip(whole_seqs, num_parts):

        out_fn = s + ".txt"
        for i in range(0, p + 1):
            key = "{}_{:02d}".format(s, i)

            if key in transcriptions:
                t_list = transcriptions[key]

                single_file = os.path.join(config.subseq_transcript_dir, key + ".txt")
                print single_file
                if os.path.isfile(single_file):
                    continue

                min_distance, t = clean_and_compare_transcripts(t_list, key)

                if min_distance < 0:
                    single_file = os.path.join(config.error_transcript_dir, key + ".txt")
                    error_exists = True

                with open(single_file, 'w') as f:
                    for l in t.splitlines():
                        l_clean = l.replace('"', '')
                        if len(l_clean) > config.long_string_warning:
                            print "long string: " + l_clean
                        f.write(l_clean + '\n\n')
            else:
                print 'subseq {} missing'.format(key)

    if error_exists:
        return True

    for s, p in zip(whole_seqs, num_parts):

        out_fn = s + ".txt"
        with open(os.path.join(config.youtube_transcript_dir, out_fn), 'w') as f:

            for i in range(0, p + 1):
                key = "{}_{:02d}".format(s, i)

                single_file = os.path.join(config.subseq_transcript_dir, key + ".txt")

                with open(single_file, 'r') as f_single:
                    f.write(f_single.read())

    gt_wildcard = os.path.join(config.ground_truth_dir, "*")
    for f_path in glob(gt_wildcard):
        out_fn = os.path.split(f_path)[-1]
        out_f_path = os.path.join(config.youtube_transcript_dir, out_fn)
        copyfile(f_path, out_f_path)

    return False




