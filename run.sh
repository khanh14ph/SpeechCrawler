#!/bin/bash

# Base directory
BASE_DIR="/home4/khanhnd/youtube_crawler/SpeechCrawler"

# Define language as a variable
LANGUAGE="vi"

# Create the output directory if it doesn't exist
mkdir -p ${BASE_DIR}/crawled/${LANGUAGE}

# Loop from 1 to 21
for i in $(seq 1 21); do
  echo "Processing file ${i}..."
  
  # Run the get_link.py script
  python ${BASE_DIR}/get_link.py ${BASE_DIR}/name_lst/${i}.txt --language vi
  
  # Concatenate the resulting files
  cat link_list0.txt link_list1.txt link_list2.txt link_list3.txt link_list4.txt link_list5.txt > ${BASE_DIR}/crawled/${LANGUAGE}/${i}.txt
  
  python to_url.py ${BASE_DIR}/crawled/${LANGUAGE}/${i}.txt
  while read url; do
  yt-dlp -x --audio-format wav --postprocessor-args "-ac 1 -ar 16000" -o "downloaded_audio/%(id)s.%(ext)s" "$url"
done < urls.txt
  echo "Completed processing file ${i}"
done
python dur.py ${BASE_DIR}/crawled/${LANGUAGE}

echo "All processing complete!"