import csv
from glob import glob
import os
from shutil import copyfile

import config

def process_transcripts():

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

                transcriptions[sub_seq] = trans

                seq_id = sub_seq[0:-3]
                subseq_id = int(sub_seq[-2:])

                if seq_id not in whole_seqs:
                    whole_seqs.append(seq_id)
                    num_parts.append(subseq_id)
                else:
                    file_idx = whole_seqs.index(seq_id)
                    if subseq_id > num_parts[file_idx]:
                        num_parts[file_idx] = subseq_id

    for s, p in zip(whole_seqs, num_parts):
        out_fn = s + ".txt"
        with open(os.path.join(config.youtube_transcript_dir, out_fn), 'w') as f:
            for i in range(0, p + 1):
                key = "{}_{:02d}".format(s, i)
                if key in transcriptions:
                    t = transcriptions[key]
                    for l in t.splitlines():
                        l_clean = l.replace('"', '')
                        if len(l_clean) > config.long_string_warning:
                            print "long string: " + l_clean
                        f.write(l_clean + '\n\n')
                else:
                    print 'subseq {} missing'.format(key)

    gt_wildcard = os.path.join(config.ground_truth_dir, "*")
    for f_path in glob(gt_wildcard):
        out_fn = os.path.split(f_path)[-1]
        out_f_path = os.path.join(config.youtube_transcript_dir, out_fn)
        copyfile(f_path, out_f_path)





