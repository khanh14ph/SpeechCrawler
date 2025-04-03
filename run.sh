#!/bin/bash

# Base directory
BASE_DIR="/Users/khanh/dev/SpeechCrawler"
LANGUAGE="vi"
if [ ! -d "downloaded_audio" ]; then
    mkdir -p downloaded_audio
    echo "Directory 'downloaded_audio' created successfully."
else
    echo "Directory 'downloaded_audio' already exists."
fi

if [ ! -d "downloaded_subtitle" ]; then
    mkdir -p downloaded_subtitle
    echo "Directory 'downloaded_subtitle' created successfully."
else
    echo "Directory 'downloaded_subtitle' already exists."
fi

if [ ! -d "crawled" ]; then
    mkdir -p crawled
    echo "Directory 'crawled' created successfully."
else
    echo "Directory 'crawled' already exists."
fi

if [ ! -d ${BASE_DIR}/crawled/${LANGUAGE} ]; then
    mkdir -p ${BASE_DIR}/crawled/${LANGUAGE}
    echo "Directory crawled/${LANGUAGE} created successfully."
else
    echo "Directory crawled/${LANGUAGE} already exists."
fi
# Define language as a variable


# Create the output directory if it doesn't exist
mkdir -p ${BASE_DIR}/crawled/${LANGUAGE}

# Loop from 1 to 21
for i in $(seq 1 21); do
  echo "Processing file ${i}..."
  
  # Run the get_link.py script
  python ${BASE_DIR}/get_link.py ${BASE_DIR}/name_lst/${i}.txt --language ${LANGUAGE}
  
  # Concatenate the resulting files
  cat links/link_list0.txt links/link_list1.txt links/link_list2.txt links/link_list3.txt links/link_list4.txt links/link_list5.txt > ${BASE_DIR}/crawled/${LANGUAGE}/${i}.txt
  
  python to_url.py ${BASE_DIR}/crawled/${LANGUAGE}/${i}.txt
  
  # Check if urls.txt is empty
  if [ ! -s urls.txt ]; then
    echo "No URLs found in urls.txt for file ${i}. Stopping execution."
    exit 1
  fi
  
  # Process URLs if the file is not empty
  while read url; do
    yt-dlp -x --audio-format wav --postprocessor-args "-ac 1 -ar 16000" -o "downloaded_audio/%(id)s.%(ext)s" "$url"
  done < urls.txt
  
  echo "Completed processing file ${i}"
done

python dur.py ${BASE_DIR}/crawled/${LANGUAGE}

echo "All processing complete!"