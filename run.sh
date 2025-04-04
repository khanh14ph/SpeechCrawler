#!/bin/bash
set -e
# Base directory
BASE_DIR="/Users/khanh/dev/crawler/SpeechCrawler"
LANGUAGE="vi"
DATABASE="/Users/khanh/dev/crawler/database"
if [ ! -d $DATABASE ]; then
    mkdir -p $DATABASE
    echo "Directory $DATABASE created successfully."
else
    echo "Directory $DATABASE already exists."
fi
if [ ! -d $BASE_DIR/links ]; then
    mkdir -p $BASE_DIR/links
    echo "Directory $BASE_DIR/links created successfully."
else
    echo "Directory $DATABASE/links already exists."
fi
if [ ! -d $DATABASE/downloaded_audio ]; then
    mkdir -p $DATABASE/downloaded_audio
    echo "Directory $DATABASE/downloaded_audio created successfully."
else
    echo "Directory $DATABASE/downloaded_audio already exists."
fi

if [ ! -d $DATABASE/downloaded_subtitle ]; then
    mkdir -p $DATABASE/downloaded_subtitle
    echo "Directory $DATABASE/downloaded_subtitle' created successfully."
else
    echo "Directory $DATABASE/downloaded_subtitle' already exists."
fi


if [ ! -d $DATABASE/downloaded_audio/$LANGUAGE ]; then
    mkdir -p $DATABASE/downloaded_audio/$LANGUAGE
    echo "Directory $DATABASE/downloaded_audio/$LANGUAGE created successfully."
else
    echo "Directory $DATABASE/downloaded_audio/$LANGUAGE already exists."
fi

if [ ! -d $DATABASE/downloaded_subtitle/$LANGUAGE ]; then
    mkdir -p $DATABASE/downloaded_subtitle/$LANGUAGE
    echo "Directory $DATABASE/downdownloaded_subtitleloaded_audio/$LANGUAGE created successfully."
else
    echo "Directory $DATABASE/downloaded_subtitle/$LANGUAGE already exists."
fi

# Define language as a variable


# Loop from 1 to 21
for i in $(seq 1 21); do
  echo "Processing file ${i}..."
  
  # Run the get_link.py script
  python ${BASE_DIR}/get_link.py ${BASE_DIR}/name_lst/${i}.txt --language ${LANGUAGE} --download_subtitle_folder $DATABASE/downloaded_subtitle
  
  # Concatenate the resulting files
  cat links/link_list0.txt links/link_list1.txt links/link_list2.txt links/link_list3.txt links/link_list4.txt links/link_list5.txt > ${BASE_DIR}/urls.txt
  
  
  # Check if urls.txt is empty
  if [ ! -s urls.txt ]; then
    echo "No URLs found in urls.txt for file ${i}. Stopping execution."
    exit 1
  fi
  
  # Process URLs if the file is not empty
  while read url; do
    yt-dlp -x --audio-format wav --postprocessor-args "-ac 1 -ar 16000" -o "$DATABASE/downloaded_audio/$LANGUAGE/%(id)s.%(ext)s" "$url"
  done < urls.txt
  
  echo "Completed processing file ${i}"
done

python dur.py ${BASE_DIR}/crawled/${LANGUAGE}

echo "All processing complete!"