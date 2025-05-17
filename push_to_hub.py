import os
from datasets import Dataset, Audio, Features, Value, Sequence
import glob
import json
from tqdm import tqdm
from dotenv import load_dotenv
import sys
import pandas as pd
import numpy as np
import librosa
from huggingface_hub import HfApi
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

LANGUAGE = "zh-Hans"
max_duration_in_second=7200  # Adjust based on your memory constraints

REPO_ID = "leduckhai/MultiMed-WS"
OUTPUT_DIR = f"{DATABASE}/{LANGUAGE}"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Find all relevant audio files based on language
all_jsonl_file = glob.glob(f"{DATABASE}/downloaded_subtitle/*.jsonl")
all_jsonl_file = sorted(all_jsonl_file)
print(f"Finding {LANGUAGE} audio files with subtitles...")

data_list = []
for i in tqdm(all_jsonl_file):
    with open(i) as f:
        info = json.load(f)
    if info["language"] == LANGUAGE:
        audio_path = f"{DATABASE}/downloaded_audio/{info['id']}.wav"
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

print(f"Processing {total_samples} samples in {num_chunks} chunks...")

api = HfApi()
from huggingface_hub import HfFileSystem
fs = HfFileSystem()
existed_files = fs.glob(f"datasets/leduckhai/MultiMed-WS/{LANGUAGE}/*")
existed_files = [os.path.basename(file) for file in existed_files]
# existed_files = []
print(existed_files)
chunk_idx=0
idx=0
total_duration=0
audio_data = []
subtitles = []
titles = []
phrases = []
ids = []
languages = []
    
while idx < total_samples: 
    
    chunk_temp=[]
    if f"chunk_{chunk_idx}.parquet" in existed_files:
        print(f"Chunk {chunk_idx} already exists, skipping...")
        continue
    data_d
    print(f"Processing chunk {chunk_idx+1}/{num_chunks} (samples {start_idx+1}-{end_idx})...")
    
    # Create dictionaries for each column

    # Load audio data for this chunk
    itemp=data_list[idx]

        # Load audio data directly
    audio_array, sampling_rate = librosa.load(item["audio_path"], sr=16000)
    length_duration=len(audio_array)/sampling_rate
    total_duration+=length_duration
    length=len(audio_array)/(sampling_rate*3600)
    if length > 3:
        continue
    if total_duration > max_duration_in_second or idx==total_samples-1:
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
        import glob
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
        audio_data = []
        subtitles = []
        titles = []
        phrases = []
        ids = []
        languages = []
        
    
    audio_data.append({"array": audio_array, "sampling_rate": sampling_rate})
    
    # Add other metadata
    subtitles.append(item["subtitle"])
    titles.append(item["title"])
    phrases.append(item["phrase_index"])
    ids.append(item["id"])
    languages.append(item["language"])

    # Create dataset for this chunk
    
    
    

print("All chunks processed and uploaded successfully")
