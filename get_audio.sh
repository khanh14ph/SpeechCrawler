#!/bin/bash
source ./.env
python start_download.py ${DATABASE}/downloaded_subtitle ${DATABASE}/downloaded_audio ${LANGUAGE}

while read url; do
    yt-dlp -x --audio-format wav --postprocessor-args "-ac 1 -ar 16000" --download-archive downloaded_urls.txt -o "$DATABASE/downloaded_audio/%(id)s.%(ext)s" "$url" \
    # --sleep-requests 1.25 --min-sleep-interval 60 --max-sleep-interval 90
    
done < temp_url.txt