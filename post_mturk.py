import config

from merge_transcripts import process_transcripts
from remove_newlines import remove_newlines_from_transcripts
from align_aeneas import align_aeneas



print "merging and processing mturk transcripts"
process_transcripts()
remove_newlines_from_transcripts()

if config.use_aeneas:
	print "aliging transcripts with audio"
	align_aeneas()
	




