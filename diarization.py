# 1. visit hf.co/pyannote/speaker-diarization and accept user conditions
# 2. visit hf.co/pyannote/segmentation and accept user conditions
# 3. visit hf.co/settings/tokens to create an access token
# 4. instantiate pretrained speaker diarization pipeline
from pyannote.audio import Pipeline
from dotenv import load_dotenv
import os

load_dotenv()

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                    use_auth_token=os.getenv("HF_TOKEN"))


from pyannote.audio.pipelines.utils.hook import ProgressHook
with ProgressHook() as hook:
    diarization = pipeline("/Users/khanh/dev/crawler/SpeechCrawler/output/Ygh9nWZNxl8/audio.wav", min_speakers=2, max_speakers=5, hook=hook)
with open("audio.rttm", "w") as rttm:
    diarization.write_rttm(rttm)