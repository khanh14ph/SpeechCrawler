# Speech-Crawler: Automatic Dataset Construction for Speech Recognition from YouTube Videos

This tool automates the process of building datasets for speech recognition by crawling audio and metadata from YouTube videos. Below are the detailed instructions to set up and run the crawler.

---

## Important Notes
- **Using Cookies**: If you use cookies to bypass age restrictions, be cautious. Excessive crawling with the same cookies may lead to a temporary ban of your YouTube account. It is recommended to avoid using cookies if possible. You can modify the `getlink.py` file and the `yt-dlp` script in `get_audio` to exclude the `--cookies cookies.txt` argument to reduce the risk of being banned.
- **IP Ban Issues**: If you encounter continuous "video not available" errors during `get_metadata` or `get_audio` steps, it might be due to YouTube banning your IP. Enable Cloudflare Warp (1.1.1.1) to resolve this issue and continue crawling.

---

## Cookie Authentication for Age-Restricted Videos
Some videos on YouTube are age-restricted and cannot be accessed without authentication. To access these videos, you need to export cookies from a browser where you are logged in and have access to the desired video.

### Steps to Export Cookies:
1. Use a browser extension to export cookies:
   - For Chrome/Edge: Use the [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en) extension and select "Netscape" format during export.
   - For Firefox: Use the [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt) extension.
2. Save the exported cookies to a file named `cookies.txt`.
3. Place the `cookies.txt` file in the same directory as `get_metadata.sh`.

---

## Step-by-Step Guide to Running the Crawler

### Step 1: Set Up Environment Variables
Create a `.env` file in the project directory with the following content:
LANGUAGE="de"
BASE_DIR="/Users/khanh/dev/crawler/SpeechCrawler"
NAME_LST_FOLDER=/Users/khanh/dev/crawler/SpeechCrawler/keywords/${LANGUAGE}
DATABASE="/Users/khanh/dev/crawler/database"

Copy
- Replace `LANGUAGE` with the desired language code (e.g., "de" for German). You can find supported language codes at [SearchAPI Documentation](https://www.searchapi.io/docs/parameters/youtube-transcripts/lang).
- Update the paths (`BASE_DIR`, `NAME_LST_FOLDER`, `DATABASE`) to match your local setup.

---

### Step 2: Create Keyword Files
Run the following command to create a folder structure for storing keywords or search queries:
python mkdir_keywords.py

Copy
After running this command, manually add your keywords or search queries into the folder specified by `NAME_LST_FOLDER` in your `.env` file.

---

### Step 3: Crawl Metadata and Audio
#### 3.1. Crawl Metadata
Run the following command to fetch metadata for videos based on your keywords:
bash get_metadata.sh

Copy
- This step collects metadata for videos and saves it to a folder.
- **Note**: This process does not support resuming if interrupted, so avoid stopping the script. Fortunately, it runs quickly as it only fetches metadata.

#### 3.2. Download Audio
Once metadata is collected, download the audio files using:
bash get_audio.sh

Copy
- This step takes longer as it downloads audio content.
- **Note**: You can interrupt this process and resume downloading later.

---

### Step 4: Upload Data to Hugging Face
Push the collected data to a Hugging Face repository in Parquet format using:
python push_to_hub.py <hf_token>

Copy
- Replace `<hf_token>` with your Hugging Face API token.
- This script supports resuming uploads, so you can stop and continue later if needed.

---

## Optional Steps
- **Delete Local Data**: To delete all local data for a specific language, run:
python delete_local.py

Copy
- **Delete Remote Data**: To delete data from a Hugging Face repository based on a pattern (useful for correcting upload errors), run:
python delete_remote.py <hf_token>

Copy
- **Calculate Duration**: To check the total duration of crawled data, run:
python get_dur.py

Copy

---

## Loading the Dataset
To load the dataset from Hugging Face for use in your projects, use the following Python code:
```python
from datasets import load_dataset
dataset = load_dataset("leduckhai/MultiMed-WS", data_dir="vi", verification_mode="no_checks", split="train")
