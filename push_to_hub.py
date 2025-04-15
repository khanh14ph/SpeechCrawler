from huggingface_hub import HfApi
import os
import glob
import json
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm
from dotenv import load_dotenv
import soundfile as sf

# Load environment variables from .env file
load_dotenv()

# Access environment variables
DATABASE = os.environ.get('DATABASE')
TOKEN = os.environ.get('TOKEN')
LANGUAGE = "vi"

# Find all relevant audio files based on language
all_jsonl_file = glob.glob(f"{DATABASE}/downloaded_subtitle/*.jsonl")
audio_metadata = []

for i in all_jsonl_file:
    with open(i) as f:
        info = json.load(f)
    if info["language"] == LANGUAGE:
        audio_path = f"{DATABASE}/downloaded_audio/{info['id']}.wav"
        if os.path.exists(audio_path):
            # Add metadata and file path to our list
            metadata = {
                "id": info['id'],
                "language": info["language"],
                "audio_path": audio_path,
                # Add any other metadata from the info dict
            }
            audio_metadata.append(metadata)

# Login to Hugging Face
api = HfApi()
repo_id = "leduckhai/MultiMed-WS"
repo_type = "dataset"

# Process files in batches of 500
batch_size = 500
total_files = len(audio_metadata)
num_batches = (total_files + batch_size - 1) // batch_size

for batch_idx in range(num_batches):
    start_idx = batch_idx * batch_size
    end_idx = min((batch_idx + 1) * batch_size, total_files)
    batch_metadata = audio_metadata[start_idx:end_idx]
    
    # Create a list to store audio data and metadata
    batch_data = []
    
    for item in tqdm(batch_metadata, desc=f"Processing batch {batch_idx+1}/{num_batches}"):
        # Read audio file
        audio_data, sample_rate = sf.read(item["audio_path"])
        
        # Convert to bytes for storage in Parquet
        audio_bytes = audio_data.tobytes()
        
        # Create entry with audio data and metadata
        entry = {
            "id": item["id"],
            "language": item["language"],
            "audio_data": audio_bytes,
            "sample_rate": sample_rate,
            "original_path": item["audio_path"],
            # Add any other metadata you want to include
        }
        batch_data.append(entry)
    
    # Create DataFrame
    df = pd.DataFrame(batch_data)
    
    # Create Parquet file
    parquet_filename = f"audio_batch_{batch_idx+1}_{LANGUAGE}.parquet"
    df.to_parquet(parquet_filename)
    
    # Upload to Hugging Face
    path_in_repo = f"audio_data/{LANGUAGE}/{parquet_filename}"
    
    try:
        api.upload_file(
            path_or_fileobj=parquet_filename,
            path_in_repo=path_in_repo,
            repo_id=repo_id,
            repo_type=repo_type,
            commit_message=f"Upload batch {batch_idx+1} of {LANGUAGE} audio files",
            token=TOKEN
        )
        print(f"Successfully uploaded {parquet_filename} with {len(batch_data)} audio files")
    except Exception as e:
        print(f"Error uploading {parquet_filename}: {e}")
    
    # Optionally remove the local parquet file after upload
    os.remove(parquet_filename)

print(f"Upload complete: {total_files} files processed in {num_batches} batches.")
