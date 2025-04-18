from datasets import Dataset, Audio
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

# Get token and folder from command line arguments
if len(sys.argv) > 1:
    TOKEN = sys.argv[1]
else:
    print("Error: Please provide a Hugging Face token and folder path as command line arguments")
    sys.exit(1)
    
LANGUAGE = "de"
CHUNK_SIZE = 100  # Adjust based on your memory constraints

# Find all relevant audio files based on language
all_jsonl_file = glob.glob(f"{DATABASE}/downloaded_subtitle/*.jsonl")
print(f"Finding {LANGUAGE} audio files with subtitles...")

audio_paths = []
metadata = []
for i in tqdm(all_jsonl_file):
    with open(i) as f:
        info = json.load(f)
    if info["language"] == LANGUAGE:
        audio_path = f"{DATABASE}/downloaded_audio/{info['id']}.wav"
        if os.path.exists(audio_path):
            metadata.append(info)
            audio_paths.append(audio_path)

print(f"Found {len(audio_paths)} audio files for language {LANGUAGE}")

# Process and upload in chunks
output_folder = f"{DATABASE}/temp"
os.makedirs(output_folder, exist_ok=True)

# Initialize Hugging Face API
api = HfApi()
# Process in chunks
for chunk_idx in range(0, len(audio_paths), CHUNK_SIZE):
    print(f"Processing chunk {chunk_idx//CHUNK_SIZE + 1}/{(len(audio_paths)-1)//CHUNK_SIZE + 1}")
    
    # Get chunk of data
    chunk_paths = audio_paths[chunk_idx:chunk_idx + CHUNK_SIZE]
    chunk_metadata = metadata[chunk_idx:chunk_idx + CHUNK_SIZE]
    
    # Load audio files for this chunk
    audio_arrays = []
    for path in tqdm(chunk_paths, desc="Loading audio files"):
        try:
            audio, sr = librosa.load(path, sr=None)
            audio_arrays.append(audio)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            # Add a placeholder or skip this file
            audio_arrays.append(np.zeros(1000))  # Small placeholder array
    
    # Create dataset for this chunk
    data_dict = {
        "audio": audio_arrays,
        "metadata": chunk_metadata,
    }
    
    chunk_dataset = Dataset.from_dict(data_dict)
    
    # Clean up previous parquet files
    for old_file in glob.glob(f"{output_folder}/*.parquet"):
        os.remove(old_file)
    
    # Save this chunk to parquet
    chunk_file = f"{output_folder}/data_chunk_{chunk_idx//CHUNK_SIZE}.parquet"
    chunk_dataset.to_parquet(chunk_file)
    
    # Upload this chunk to Hugging Face
    chunk_folder_name = f"chunk_{chunk_idx//CHUNK_SIZE}"
    print(f"Uploading chunk {chunk_idx//CHUNK_SIZE + 1} to Hugging Face...")
    
    api.upload_folder(
        folder_path=output_folder,
        repo_id="leduckhai/MultiMed-WS",  # Replace with your actual repo
        repo_type="dataset",
        path_in_repo=f"{LANGUAGE}/{chunk_folder_name}",token=TOKEN,
    )
    
    print(f"Chunk {chunk_idx//CHUNK_SIZE + 1} uploaded successfully")
    
    # Free up memory
    del chunk_dataset
    del audio_arrays
    del data_dict

print("All chunks processed and uploaded successfully")
