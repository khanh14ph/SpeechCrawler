#!/bin/bash
set -e
# Base directory
source ./.env
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



# Define language as a variable


# Loop from 1 to 21
for i in $(seq 1 21); do
  echo "Processing file ${i}..."
  
  # Run the get_link.py script
  python ${BASE_DIR}/get_link.py ${NAME_LST_FOLDER}/${i}.txt --language ${LANGUAGE} --download_folder $DATABASE --index ${i}
  
  # Concatenate the resulting files
  

done

echo "Completed crawl metadata"