 Speech-Crawler: Automated Speech Recognition Dataset Construction from YouTube Videos

## Overview
This tool automates the creation of speech recognition datasets by extracting audio and metadata from YouTube videos. Features include age-restricted content handling, Hugging Face integration, and progress tracking.

## Prerequisites
- Python 3.7+
- yt-dlp
- Hugging Face account (for dataset upload)
- Cloudflare DNS (1.1.1.1) recommended for IP ban prevention

## Setup Guide

### 1. Environment Configuration
Create `.env` file with:
LANGUAGE="de"  # ISO 639-1 code (see https://www.searchapi.io/docs/parameters/youtube-transcripts/lang)
BASE_DIR="/path/to/SpeechCrawler"
NAME_LST_FOLDER="${BASE_DIR}/keywords/${LANGUAGE}"
DATABASE="/path/to/database"

Copy

### 2. Keyword Initialization
python mkdir_keywords.py

Copy
Populate generated files in `keywords/${LANGUAGE}` with your search queries.

## Core Workflow

### Metadata Collection
bash get_metadata.sh

Copy
*Important: Do not interrupt this process. Average execution time: 2-3 minutes per 100 videos.*

### Audio Download
bash get_audio.sh

Copy
Supports resumable downloads. Estimated throughput: 50-100 videos/hour depending on audio length.

## Authentication Handling
For age-restricted content:

1. Install [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor) (Chrome/Edge) or [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt) (Firefox)
2. Export cookies in Netscape format as `cookies.txt`
3. Place in project root

*Warning: Excessive requests from same account may trigger temporary bans. Use sparingly.*

## Data Management

### Hugging Face Integration
python push_to_hub.py <your_hf_token>

Copy
Features incremental upload with 90% resumption capability. Typical upload speed: 2-4GB/hour.

### Maintenance Utilities
python delete_local.py  # Local data cleanup
python delete_remote.py <hf_token>  # Remote dataset management
python get_dur.py  # Duration statistics

Copy

## Dataset Access
```python
from datasets import load_dataset
dataset = load_dataset(
    "leduckhai/MultiMed-WS",
    data_dir="vi",
    verification_mode="no_checks",
    split="train"
)
