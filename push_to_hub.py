from huggingface_hub import HfApi
import os
import glob
import shutil
import zipfile
import os
from tqdm import tqdm
from dotenv import load_dotenv
import glob
# Load environment variables from .env file
load_dotenv()

# Now you can access them with os.environ
DATABASE = os.environ.get('DATABASE')
TOKEN = os.environ.get('TOKEN')
LANGUAGE = os.environ.get('LANGUAGE')
# LANGUAGE="vi"
all_jsonl_file=glob.glob(f"{DATABASE}/downloaded_subtitle/*.jsonl")
res=[]
import json
for i in all_jsonl_file:
    info=json.load(open(i))
    if info["language"]==LANGUAGE:
        audio_path=f"{DATABASE}/downloaded_audio/{info['id']}.wav"
        res.append(audio_path)

# Login to Hugging Face
api = HfApi()  # Get token from https://huggingface.co/settings/tokens

wav_files = res


for wav_file in wav_files:
    # Extract just the filename
    filename = os.path.basename(wav_file)
    
    print(f"Uploading {filename}...")
    
    # Upload to the destination folder in your repo
    api.upload_file(
        path_or_fileobj=wav_file,
        path_in_repo=f"audio_data/{LANGUAGE}/{filename}",  # Change 'audio_data' to your preferred folder name
        repo_id="leduckhai/MultiMed-WS",
        repo_type="dataset",  # or "model" if it's a model repo
        commit_message=f"Upload {filename}",
        token=TOKEN
    )
    
print("All WAV files uploaded successfully!")