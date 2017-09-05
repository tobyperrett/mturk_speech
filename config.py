# settings
use_aeneas = True
use_youtube = False


min_silence_len = 2000
chunk_separation = 1000
chunk_extension = 'wav'
save_seq_length_secs = 30

video_extension = 'mp4'

n_mturk_runs = 3

server_address = 'http://bristolengineeringsurvey.esy.es/audio/'
csv_first_line = "media-link"
max_seqs_per_csv = 10000000
ignore_gt_annotations = True

max_levenshtein = 0

# not used yet - should probably implement for aeneas and split_silence
num_threads = 4

# directories
mturk_input_dir = 'mturk_input'
narrations_subfolder = 'narrations'
mturk_results_dir = 'mturk_results'
subseq_transcript_dir = "tmp_short_transcripts"
error_transcript_dir = "tmp_error_transcripts"
aeneas_transcript_dir = 'transcripts_no_newline'
youtube_transcript_dir = 'transcripts'
youtube_download_dir = 'subtitles_downloads'
aeneas_output_dir = 'DONE_aeneas'
youtube_output_dir = 'DONE_youtube'
ground_truth_dir = 'ground_truths'

# person specific information
# PIDs = ['P02', 'P03', 'P09', 'P11']
# thresholds = [-40, -40, -35, -35]
# audio_file_extensions = ['mp3', 'm4a', 'm4a', 'm4a']

PIDs = ['P06']
thresholds = [-35]
audio_file_extensions = ['m4a']

# PIDs = ['P06']
# thresholds = [ -40]
# audio_file_extensions = ['m4a']


# for use when renaming downloaded youtube captions
# must correspond to the PIDs above
# caption_starts = [0, 27, 42, 50] 

# misc
black_img = 'black.jpg'
long_string_warning = 50


