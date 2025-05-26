"""
library yt_dlp hasn't supported to choose the dubbed version yet, so this sucks!
"""

import glob
import sys
import json
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

# Get filename from command line arguments
if len(sys.argv) > 1:
    folder_subtitle = sys.argv[1]
    folder_audio = sys.argv[2]
    language = sys.argv[3]
else:
    print("Error: Please provide <subtitle folder>, <audio folder>, and <language> as arguments")
    sys.exit(1)

import os
subtitle_lst = os.listdir(folder_subtitle)

audio_lst=os.listdir(f"{folder_audio}")
audio_lst=[i[:-4] for i in audio_lst]

# Load previously attempted downloads
lst = []
attempted_to_download = open("downloaded_urls.txt", "r", encoding="utf-8").read().splitlines()
attempted_to_download = [i.split()[-1] for i in attempted_to_download if i.strip()]

# Function to check if a YouTube video has audio in target language
def has_target_language_audio(video_id, target_lang):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "forcejson": True,
        "simulate": True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            # Check audio track language
            for fmt in info.get("formats", []):
                if fmt.get("asr") and fmt.get("language") == target_lang:
                    return True
            # Fallback to metadata
            if info.get("language") == target_lang:
                return True
    except DownloadError as e:
        print(f"[!] Failed to analyze {video_id}: {e}")
    return False

#loop over archived subtitle files to download not-yet url
for i in subtitle_lst:
    d = json.load(open(f"{folder_subtitle}/{i}", encoding="utf-8"))
    video_id = d["id"]
    if d["language"] == language and video_id not in audio_lst and video_id not in attempted_to_download:
        # Check if audio in target language
        if has_target_language_audio(video_id, language):
            lst.append(i[:-6])
        else:
            print(f"[-] Skipped {video_id}: audio not in target language")

print("Need to download:", len(lst))

with open("temp_url.txt", "w", encoding="utf-8") as f:
    for i in lst:
        f.write(f"https://www.youtube.com/watch?v={i}\n")
