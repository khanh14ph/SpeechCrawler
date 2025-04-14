import zipfile
import os
from tqdm import tqdm
from dotenv import load_dotenv
import glob
# Load environment variables from .env file
load_dotenv()

# Now you can access them with os.environ
DATABASE = os.environ.get('DATABASE')
# LANGUAGE = os.environ.get('LANGUAGE')
LANGUAGE="vi"
def zip_files(file_list, output_zip_name):
    """
    Zip a list of files into a single zip archive
    
    Args:
        file_list (list): List of file paths to zip
        output_zip_name (str): Name of the output zip file
    """
    with zipfile.ZipFile(output_zip_name, 'w') as zipf:
        for file in tqdm(file_list):
            if os.path.isfile(file):
                zipf.write(file, os.path.basename(file))
                print(f"Added {file} to {output_zip_name}")
            else:
                print(f"Warning: {file} not found or not a file")
all_jsonl_file=glob.glob(f"{DATABASE}/downloaded_subtitle/*.jsonl")
res=[]
import json
for i in all_jsonl_file:
    info=json.load(open(i))
    if info["language"]==LANGUAGE:
        audio_path=f"{DATABASE}/downloaded_audio/{info['id']}.wav"
        res.append(audio_path)
os.makedirs(f"{DATABASE}/zip_files",exist_ok=True)
zip_files(res, f"{DATABASE}/zip_files/{LANGUAGE}.zip")