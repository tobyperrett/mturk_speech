from glob import glob
import subprocess
import os
import config

def remove_newlines_from_transcripts():

	for fn in glob(os.path.join(config.youtube_transcript_dir, "*.txt")):
		file_name = os.path.split(fn)[1]
		out_file = os.path.join(config.aeneas_transcript_dir, file_name)
		# print out_file

		with open(out_file, 'w') as o:
			cmd = ["sed", '/^\s*$/d', fn]
			subprocess.call(cmd, stdout=o)
