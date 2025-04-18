from huggingface_hub import HfApi
from tqdm import tqdm
from dotenv import load_dotenv
import soundfile as sf
import sys
# Load environment variables from .env file
load_dotenv()

# Access environment variables

api = HfApi()
repo_id = "leduckhai/MultiMed-WS"
repo_type = "dataset"
# Get filename from command line arguments
if len(sys.argv) > 1:
    TOKEN = sys.argv[1]
else:
    print("Error: Please provide a filename as a command line argument")
    sys.exit(1)
api.delete_files(
            delete_patterns="data/*",
            repo_id=repo_id,
            repo_type=repo_type,
            token=TOKEN
        )