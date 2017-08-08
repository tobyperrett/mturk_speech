import config
from split_silence import split_all
from generate_mturk_csvs import generate_csvs
from create_youtube_videos import create_all_videos

print "splitting audio files"
split_all()

if config.use_youtube:
	print "generating youtube videos"
	create_all_videos()


print "generating mturk csvs"
generate_csvs()
	



