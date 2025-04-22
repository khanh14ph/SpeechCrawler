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
import glob

# Load environment variables from .env file
load_dotenv()

# Access environment variables
DATABASE = os.environ.get('DATABASE')
language="vi"
metadata_lst=glob.glob(f"{DATABASE}/downloaded_subtitle/*.jsonl")
for i in tqdm(metadata_lst):
    with open(i, 'r') as f:
        metadata = json.load(f)
        if metadata["language"]==language:
            audio_path = f"{DATABASE}/downloaded_audio/{metadata['id']}.wav"
            if os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"Deleted {audio_path}")
            else:
                print(f"File {audio_path} does not exist")
        else:
            print(f"File does not exist")  
    