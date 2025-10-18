# YouTube Video Crawler

A comprehensive Python tool to crawl and download all data from YouTube videos using yt-dlp.

## Features

- **Transcription Extraction**: Automatically downloads manual subtitles (preferred) or auto-generated captions from Google
- **Speaker Diarization**: Add speaker labels to transcript segments using pyannote.audio diarization results
- **Video Metadata**: Extracts title, description, uploader, views, likes, tags, and more
- **Audio Download**: Downloads audio in 16kHz mono WAV format (optimized for speech processing)
- **Video Download**: Downloads video in best available quality (MP4 format)
- **Structured Output**: Organizes all data by video ID with JSON metadata

## Requirements

- Python 3.7+
- FFmpeg (for audio/video processing)
- yt-dlp (loaded from `/Users/khanh/dev/crawler/yt-dlp`)

### Installing FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure yt-dlp is available at `/Users/khanh/dev/crawler/yt-dlp`

## Usage

### Command Line

**Basic usage:**
```bash
python youtube_crawler.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Custom output directory:**
```bash
python youtube_crawler.py "https://www.youtube.com/watch?v=VIDEO_ID" -o my_downloads
```

**Skip specific downloads:**
```bash
# Skip video download (only get audio, transcript, metadata)
python youtube_crawler.py "URL" --skip-video

# Skip audio download
python youtube_crawler.py "URL" --skip-audio

# Skip transcription
python youtube_crawler.py "URL" --skip-transcript
```

**Add speaker diarization to existing results:**
```bash
# First, run speaker diarization using diarization.py to generate RTTM file
# Then add speaker IDs to transcript segments
python youtube_crawler.py --add-diarization output/VIDEO_ID/crawl_results.json audio.rttm
```

### Python API

```python
from youtube_crawler import YouTubeCrawler

# Initialize crawler
crawler = YouTubeCrawler(output_dir="output")

# Crawl everything
results = crawler.crawl("https://www.youtube.com/watch?v=VIDEO_ID")

# Or download specific components
metadata = crawler.download_metadata(url)
transcription = crawler.download_transcription(url, video_id, video_title)
audio_path = crawler.download_audio(url, video_id, video_title)
video_path = crawler.download_video(url, video_id, video_title)

# Add speaker diarization
results = crawler.add_diarization_to_results(
    'output/VIDEO_ID/crawl_results.json',
    'audio.rttm'
)
```

### Example Usage

```bash
python example_usage.py
```

## Output Structure

```
output/
└── VIDEO_ID/
    ├── metadata.json           # Video metadata
    ├── description.txt         # Video description
    ├── crawl_results.json      # Complete crawl results
    ├── transcripts/
    │   ├── VIDEO_TITLE.json3   # Raw subtitle data
    │   └── VIDEO_TITLE_transcript.txt  # Clean transcript text
    ├── audio/
    │   └── VIDEO_TITLE.wav     # 16kHz mono audio
    └── video/
        └── VIDEO_TITLE.mp4     # Video file
```

## Transcription Details

The crawler prioritizes transcription sources in this order:
1. **Manual subtitles** (human-created, most accurate)
2. **Auto-generated captions** (Google's AI-generated transcription)

Transcriptions include:
- Timing information (start time, duration for each segment)
- Full text transcript in a clean, readable format
- Both structured JSON and plain text formats

### Speaker Diarization

Add speaker labels to your transcripts using pyannote.audio:

1. **Generate diarization RTTM file** using `diarization.py`:
```python
from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="YOUR_HF_TOKEN"
)

diarization = pipeline("output/VIDEO_ID/audio.wav", min_speakers=2, max_speakers=5)

with open("audio.rttm", "w") as rttm:
    diarization.write_rttm(rttm)
```

2. **Add speaker IDs to transcript**:
```bash
python youtube_crawler.py --add-diarization output/VIDEO_ID/crawl_results.json audio.rttm
```

This will add a `speaker_id` field to each transcript segment:
```json
{
  "start": 0.06,
  "duration": 5.04,
  "text": "so you've talked a lot about the mental",
  "speaker_id": "SPEAKER_01"
}
```

## Audio Specifications

Downloaded audio is optimized for speech processing:
- **Sample Rate**: 16kHz
- **Channels**: Mono (1 channel)
- **Format**: WAV (uncompressed)

## Examples

### Download a single video with all data:
```bash
python youtube_crawler.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Download only audio and transcription (no video):
```bash
python youtube_crawler.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --skip-video
```

### Process multiple videos:
```python
from youtube_crawler import YouTubeCrawler

urls = [
    "https://www.youtube.com/watch?v=VIDEO1",
    "https://www.youtube.com/watch?v=VIDEO2",
]

crawler = YouTubeCrawler(output_dir="batch_output")

for url in urls:
    print(f"Processing: {url}")
    results = crawler.crawl(url)
    print(f"Done: {results['title']}")
```

## Troubleshooting

**"FFmpeg not found" error:**
- Install FFmpeg (see Requirements section)
- Make sure it's in your system PATH

**"No transcription available":**
- Some videos don't have captions/subtitles
- Try different language codes in the `subtitleslangs` parameter

**"yt-dlp module not found":**
- Check that `/Users/khanh/dev/crawler/yt-dlp` exists
- Or install yt-dlp via pip: `pip install yt-dlp`

## License

This tool uses yt-dlp which is open source. Please respect YouTube's Terms of Service when using this tool.
