#!/bin/bash
DATABASE="/Users/khanh/dev/crawler/database"
LANGUAGE="vi"
python start_download.py ${DATABASE}/downloaded_subtitle ${DATABASE}/downloaded_audio ${LANGUAGE}

while read url; do
    yt-dlp -x --audio-format wav --cookies cookies.txt --postprocessor-args "-ac 1 -ar 16000" --download-archive downloaded_urls.txt -o "$DATABASE/downloaded_audio/%(id)s.%(ext)s" "$url" \
    # --sleep-requests 1.25 --min-sleep-interval 60 --max-sleep-interval 90
    
done < temp_url.txt