from datasets import Dataset, Audio, Features, Value, Sequence
import os
import glob
import json
from tqdm import tqdm
from dotenv import load_dotenv
import sys
import pandas as pd
import numpy as np
import librosa
import soundfile as sf
from huggingface_hub import HfApi
import shutil

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
    
LANGUAGE = "vi"
CHUNK_SIZE = 20 # Adjust based on your memory constraints
REPO_ID = "leduckhai/MultiMed-WS"
OUTPUT_DIR = f"{DATABASE}/{LANGUAGE}"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Find all relevant audio files based on language
all_jsonl_file = glob.glob(f"{DATABASE}/downloaded_subtitle/*.jsonl")
all_jsonl_file=sorted(all_jsonl_file)
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
num_chunks = (total_samples + CHUNK_SIZE - 1) // CHUNK_SIZE  # Ceiling division

print(f"Processing {total_samples} samples in {num_chunks} chunks...")

# Define features for the dataset
# features = Features({
#     'audio': Audio(sampling_rate=16000),
#     'subtitle': Sequence({
#                 'text': Value('string'),
#                 'start': Value('float'),
#                 'duration': Value('float')
#             }),
#     'title': Value('string'),
#     'phrase_index': Value('int32'),
#     'id': Value('string'),
#     'language': Value('string')
# })

api = HfApi()
from huggingface_hub import HfFileSystem
fs = HfFileSystem()
existed_files=fs.glob(f"datasets/leduckhai/MultiMed-WS/{LANGUAGE}/*")
existed_files=[os.path.basename(file) for file in existed_files]
print(existed_files)
for chunk_idx in range(num_chunks):
    if f"chunk_{chunk_idx}.parquet" in existed_files:
        print(f"Chunk {chunk_idx} already exists, skipping...")
        continue
    start_idx = chunk_idx * CHUNK_SIZE
    end_idx = min((chunk_idx + 1) * CHUNK_SIZE, total_samples)
    
    print(f"Processing chunk {chunk_idx+1}/{num_chunks} (samples {start_idx+1}-{end_idx})...")
    
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
    # print(chunk_dataset[0]["subtitle"])
    import glob
    lst=glob.glob(f"{OUTPUT_DIR}/*")
    for w in lst:
        os.remove(w)
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
