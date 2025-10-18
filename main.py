from youtube_crawler import YouTubeCrawler
from pyannote.audio import Pipeline
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Step 1: Crawl the video
crawler = YouTubeCrawler(output_dir="output")
results = crawler.crawl("https://www.youtube.com/watch?v=scVbJntQ444")

video_id = results['video_id']
audio_path = results['audio_path']

# Step 2: Run speaker diarization
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=os.getenv("HF_TOKEN")
)

from pyannote.audio.pipelines.utils.hook import ProgressHook
with ProgressHook() as hook:
    diarization = pipeline(audio_path, hook=hook)

rttm_path = f"output/{video_id}/audio.rttm"
with open(rttm_path, "w") as rttm:
    diarization.write_rttm(rttm)

# Step 3: Add speaker IDs to transcript
results = crawler.add_diarization_to_results(
    f"output/{video_id}/crawl_results.json",
    rttm_path
)

print("✓ Complete with speaker diarization!")