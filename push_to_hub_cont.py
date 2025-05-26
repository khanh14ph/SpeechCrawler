"""
This code will automatically detect the lastest chunk existed on HF in order to continue
the work of the dataset folder.
"""

import os
from datasets import Dataset
import glob
import json
from tqdm import tqdm
from dotenv import load_dotenv
import sys, re
import pandas as pd
import numpy as np
import librosa
from huggingface_hub import HfApi, HfFileSystem
import shutil
import gc

# Load environment variables from .env file
load_dotenv()
# Access environment variables
DATABASE = os.environ.get('DATABASE')

# Get token from command line arguments
if len(sys.argv) > 1:
    TOKEN = sys.argv[1]
else:
    print("Error: Please provide a Hugging Face token as command line argument")
    sys.exit(1)

LANGUAGE = "pt"
CHUNK_SIZE = 7  # Adjust based on your memory constraints
REPO_ID = "leduckhai/MultiMed-WS"
OUTPUT_DIR = f"{DATABASE}/{LANGUAGE}"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load JSON file. Find all relevant audio files based on language
all_jsonl_file = glob.glob(f"{DATABASE}/downloaded_subtitle/*.jsonl")
all_jsonl_file = sorted(all_jsonl_file)
print(f"Finding {LANGUAGE} audio files with subtitles...")

data_list = []
for i in tqdm(all_jsonl_file):
    with open(i, encoding='utf-8') as f:
        info = json.load(f)
    if info["language"] == LANGUAGE:
        audio_path = f"{DATABASE}/downloaded_audio/bonus/{info['id']}.wav"
        if os.path.exists(audio_path):
            data_list.append({
                "audio_path": audio_path,
                "subtitle": info["subtitles"],
                "title": info["title"],
                "phrase_index": info["phrase_index"],
                "id": info["id"],
                "language": info["language"]
            })

# Process in chunks to save memory
total_samples = len(data_list)
num_chunks = (total_samples + CHUNK_SIZE - 1) // CHUNK_SIZE  # Ceiling division
print(f"Processing {total_samples} samples in {num_chunks} chunks...")

api = HfApi()
fs = HfFileSystem()
existing_files = fs.glob(f"datasets/{REPO_ID}/{LANGUAGE}/*")
existing_files = [os.path.basename(file) for file in existing_files]

#Find the max index of existing files
chunk_indices = []
pattern = re.compile(r"chunk_(\d+)\.parquet")
for f in existing_files:
    match = pattern.match(f)
    if match:
        chunk_indices.append(int(match.group(1)))

if chunk_indices:
    # start_chunk_idx = 121
    start_chunk_idx = max(chunk_indices) + 1
else:
    start_chunk_idx = 0
print(f"Last uploaded chunk on HuggingFace: {max(chunk_indices) if chunk_indices else 'None'}")
print(f"Starting new uploads from chunk {start_chunk_idx}")

for chunk_idx in range(start_chunk_idx, start_chunk_idx + num_chunks):
    if f"chunk_{chunk_idx}.parquet" in existing_files:
        print(f"Chunk {chunk_idx} already exists, skipping...")
        continue
    local_idx = chunk_idx - start_chunk_idx
    start_idx = local_idx * CHUNK_SIZE
    end_idx = min((local_idx + 1) * CHUNK_SIZE, total_samples)
    
    print(f"Processing chunk {chunk_idx+1}/{start_chunk_idx+num_chunks} (samples {start_idx+1}-{end_idx})...")
    
    chunk_data = data_list[start_idx:end_idx]

    # Create dictionaries for each column
    audio_data = []
    subtitles = []
    titles = []
    phrases = []
    ids = []
    languages = []

    # Load audio data for this chunk
    for item in tqdm(chunk_data):
        # Load audio data directly
        audio_array, sampling_rate = librosa.load(item["audio_path"], sr=16000)
        audio_data.append({"array": audio_array, "sampling_rate": sampling_rate})
        
        # Add other metadata
        subtitles.append(item["subtitle"])
        titles.append(item["title"])
        phrases.append(item["phrase_index"])
        ids.append(item["id"])
        languages.append(item["language"])

    # Create dataset for this chunk
    chunk_dict = {
        "audio": audio_data,
        "subtitle": subtitles,
        "title": titles,
        "phrase_index": phrases,
        "id": ids,
        "language": languages
    }

    chunk_dataset = Dataset.from_dict(chunk_dict)
    print("convert complete")
    
    # Remove temporary data to free memory
    del audio_data, subtitles, titles, phrases, ids, languages
    gc.collect()
    remove_lst=glob.glob(f"{OUTPUT_DIR}/*.parquet")
    for i in remove_lst:
        os.remove(i)
    # Save as parquet
    chunk_file = f"{OUTPUT_DIR}/chunk_{chunk_idx}.parquet"
    chunk_dataset.to_parquet(chunk_file)
    print(f"Saved chunk to {chunk_file}")

    # Upload all parquet files to Hugging Face
    print(f"Uploading all chunks to {REPO_ID}...")
    api.upload_folder(
        folder_path=OUTPUT_DIR,
        repo_id=REPO_ID,
        repo_type="dataset",
        path_in_repo=LANGUAGE,
        token=TOKEN
    )

print("All chunks processed and uploaded successfully")