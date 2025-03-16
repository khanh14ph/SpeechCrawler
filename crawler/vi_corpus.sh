#!/bin/bash
trap "exit" INT

target_dir=$1
filter_dir=$2
list=$3

for url in $(cat $list); do 
    echo "$url"
    yt-dlp --download-archive ./vi-downloaded.txt --no-overwrites -f 'bestaudio[ext=m4a]' --restrict-filenames --youtube-skip-dash-manifest --prefer-ffmpeg --socket-timeout 20  -iwc --write-info-json -k --write-srt --sub-format ttml --ffmpeg-location /usr/bin/ --sub-lang vi --convert-subs vtt $url -o "$target_dir%(id)s%(title)s.%(ext)s" --exec "python ./crawler/process.py {} '$filter_dir'" -4
done