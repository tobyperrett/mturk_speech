These scripts provide a method to generate subtitle files with timestamps from narration audio files using mechanical turk for transctiption and either youtube or aeneas for audio and transcription alignment.

The process is as follows:
1. Split narration files up into ~30s chunks.  Small chunks (rather than full ~10 min clips) are used as mechanical turk workers will transcribe these for less.
2. Host audio files on a server.
3. Use mechanical turk to get narration transcripts for 30s clips.
4. Merge 30s transcrips back into their full versions.
5. Align transcripts with audio.  Two methods are provided:
    - aeneas: offline, no manual work needed
    - youtube: manual video upload, transcript upload and transcript download are required for each clip



____________Assumptions:____________

1. All input will be of the form Pxx_yy, where xx is the 2 digit (zero-padded) person ID, and yy is the 2 digit (zero-padded) clip ID.  Scripts will need modifying if this changes.

2. The layout of the dataset folder is as follows:

    Top level: scripts/readme etc

        DONE_aeneas: output .sbv transcript files produced by youtube

        DONE_youtube: output .sbv transcript files produced by aeneas

        ground_truths: ground truth annotations

        mturk_input: all files necessary for mechanical turk - .csv jobfile(s) and 30s audio clips which can be copied to a file host

        mturk_results: mechanical turk completed results .csv's should be placed here

        subtitles_downloads: .sbvs from youtube should be downloaded here

        subseq_transcript_dir: temp folder for correct transcriptions
        
        error_transcript_dir = temp folder for incorrect transcriptions

        transcripts: merged transcript files are here, ready for upload to youtube (they contain a blank line between each action)

        transcripts_no_newline: merged transcript files are here, ready for use by aeneas (no blank line between each action)

        Pxx:  All videos belonging to person xx (of the form Pxx_yy.mp4) are stored here.  These videos are not required.
            
            narrations: narration audio files of the form Pxx_yy.mp3/m4a are stored here.
            


____________Requirements:____________

use pip to install numpy, aeneas, pydub

ffmpeg (if using youtube)



____________Instructions (using aeneas):____________

1. Work out silence threshold for each person.
    1.1 Manually transcribe one (mid-length) video, making sure there is a blank line between each action.
    1.2 Put the text file in the ground truth folder (to avoid it being re-annotated by mturk), with the name Pxx_yy.txt
    1.3 Run split_silence.py (e.g. python split_silence.py P02_04 mp3 -40) and listen to short.wav.  If there are words missing compared to the ground truth, reduce the silence level.  There's a tradeoff between amount of silence cut and amount of words missed.  You still want all the words to be there, even if it means more silence.

2. Fill in and check config file.
    - check folder locations/names
    - specify whether aeneas (recommended) or youtube will be used for subtitle alignment
    - fill in information about each person's narration clips - file extension (mp3 or m4a) and silence threshold are required
    - specify audio file host address
    - specify max number of jobs per batch (I recommend putting them all in one big file and paying a 20% higher fee as it's way less hassle).

3. Run aeneas_pre_mturk.py

4. Copy all .wav files in mturk_input to file host.

5. Run mechanical turk.  Upload the job .csv(s) in mturk_input folder.  When results come in, 

    **************************************************
    ***REJECT ANY WITHOUT A NEWLINE BETWEEN ACTIONS***
    **************************************************

    This ensures that they've read the instructions and is required by the next script.  Also have a quick glance over and check any ones that look suspect.

6. When you're happy with the mechanical turk results and have accepted/rejected them all, download the completed .csv to mturk_results

7. Run aeneas_post_mturk.py.



____________Instructions (using youtube)____________

1. Same as above

2. Same as above

3. Run youtube_pre_mturk.py

4. Same as above

5. Same as above

6. Same as above

7. Run youtube_post_mturk.py

8. Upload all videos to youtube (narration audio with black frames) which are in Pxx/narrations/Pxx_yy_youtube.mp4

9. For each video, go to closed captions->Add new subtitles or CC->English->Transcribe and auto sync, and paste in transcript.  You'll need to wait a few mins before downloading, so it's best to do this step for all videos, then the next step for all videos.

10. For each video, go to closed captions->English and download.

11. If 8, 9 and 10 are all done in the same numerical ascending order, which matches up with the PIDs specified in the config file then the script youtube_post_download.py will rename captions.sbv, captions(1).sbv, captions(2).sbv etc. to the correct video names and put them in the youtube done folder.  For this to work you must be using ALL videos from the PIDs specified (including ground truts), and include the index of the first downloaded captions file which corresponds to each person in the config file.


