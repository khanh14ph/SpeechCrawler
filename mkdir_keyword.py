import os
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access them with os.environ
BASE_DIR = os.environ.get('BASE_DIR')
LANGUAGE = os.environ.get('LANGUAGE')
for i in range(1,22):
    os.makedirs(f"{BASE_DIR}/keywords/{LANGUAGE}",exist_ok=True)
    with open(f"{BASE_DIR}/keywords/{LANGUAGE}/{str(i)}.txt","w",encoding="utf-8") as f:
        pass    