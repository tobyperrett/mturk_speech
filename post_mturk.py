import config

from merge_transcripts import process_transcripts
from remove_newlines import remove_newlines_from_transcripts
from align_aeneas import align_aeneas



print "merging and processing mturk transcripts"
errors_exist = process_transcripts()

if errors_exist:
	print "please clean up transcripts in {}, move them to {} and then rerun this script.".format(config.error_transcript_dir, config.subseq_transcript_dir)
	exit(0)

remove_newlines_from_transcripts()

if config.use_aeneas:
	print "aliging transcripts with audio"
	align_aeneas()
	




