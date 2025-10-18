#!/usr/bin/env python3
"""
YouTube Video Crawler using yt-dlp
Extracts: transcription (manual/auto), description, audio (16kHz mono), and video
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional, List, Tuple
import argparse

# Add yt-dlp to path
sys.path.insert(0, '/Users/khanh/dev/crawler/yt-dlp')

import yt_dlp


class YouTubeCrawler:
    def __init__(self, output_dir: str = "output"):
        """
        Initialize YouTube crawler

        Args:
            output_dir: Directory to save downloaded files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def parse_rttm_file(self, rttm_path: str) -> List[Dict]:
        """
        Parse RTTM file containing speaker diarization results

        RTTM format: SPEAKER <file> <channel> <start> <duration> <NA> <NA> <speaker_id> <NA> <NA>

        Args:
            rttm_path: Path to RTTM file

        Returns:
            List of diarization segments with start, end, and speaker_id
        """
        segments = []

        try:
            with open(rttm_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or not line.startswith('SPEAKER'):
                        continue

                    parts = line.split()
                    if len(parts) >= 8:
                        start_time = float(parts[3])
                        duration = float(parts[4])
                        speaker_id = parts[7]

                        segments.append({
                            'start': start_time,
                            'end': start_time + duration,
                            'speaker_id': speaker_id
                        })

            print(f"Parsed {len(segments)} speaker segments from RTTM file")

        except Exception as e:
            print(f"Error parsing RTTM file: {e}")

        return segments

    def add_speaker_to_transcripts(self, transcript_segments: List[Dict], diarization_segments: List[Dict]) -> List[Dict]:
        """
        Add speaker_id to each transcript segment based on time overlap with diarization

        Args:
            transcript_segments: List of transcript segments with 'start' and 'duration'
            diarization_segments: List of diarization segments with 'start', 'end', and 'speaker_id'

        Returns:
            Updated transcript segments with 'speaker_id' added
        """
        if not diarization_segments:
            print("No diarization segments available")
            return transcript_segments

        updated_segments = []

        for transcript in transcript_segments:
            transcript_start = transcript['start']
            transcript_end = transcript_start + transcript['duration']
            transcript_mid = transcript_start + (transcript['duration'] / 2)

            # Find the best matching speaker based on overlap
            best_speaker = None
            max_overlap = 0

            for diar in diarization_segments:
                # Calculate overlap between transcript and diarization segment
                overlap_start = max(transcript_start, diar['start'])
                overlap_end = min(transcript_end, diar['end'])
                overlap = max(0, overlap_end - overlap_start)

                if overlap > max_overlap:
                    max_overlap = overlap
                    best_speaker = diar['speaker_id']

                # Alternative: check if midpoint of transcript falls within diarization segment
                if diar['start'] <= transcript_mid <= diar['end']:
                    best_speaker = diar['speaker_id']
                    break

            # Create updated segment with speaker_id
            updated_segment = transcript.copy()
            updated_segment['speaker_id'] = best_speaker if best_speaker else "UNKNOWN"
            updated_segments.append(updated_segment)

        return updated_segments

    def add_diarization_to_results(self, results_file: str, rttm_file: str) -> Dict:
        """
        Add speaker diarization information to existing crawl_results.json

        Args:
            results_file: Path to crawl_results.json
            rttm_file: Path to RTTM diarization file

        Returns:
            Updated results dictionary
        """
        try:
            # Load existing results
            with open(results_file, 'r', encoding='utf-8') as f:
                results = json.load(f)

            # Parse RTTM file
            diarization_segments = self.parse_rttm_file(rttm_file)

            # Update auto_subtitles with speaker information
            if 'transcription' in results and 'auto_subtitles' in results['transcription']:
                auto_subs = results['transcription']['auto_subtitles']
                if auto_subs:
                    updated_subs = self.add_speaker_to_transcripts(auto_subs, diarization_segments)
                    results['transcription']['auto_subtitles'] = updated_subs
                    print(f"Added speaker IDs to {len(updated_subs)} auto-subtitle segments")

            # Update manual_subtitles with speaker information
            if 'transcription' in results and 'manual_subtitles' in results['transcription']:
                manual_subs = results['transcription']['manual_subtitles']
                if manual_subs:
                    updated_subs = self.add_speaker_to_transcripts(manual_subs, diarization_segments)
                    results['transcription']['manual_subtitles'] = updated_subs
                    print(f"Added speaker IDs to {len(updated_subs)} manual-subtitle segments")

            # Save updated results
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            print(f"Updated results saved to: {results_file}")

            return results

        except Exception as e:
            print(f"Error adding diarization to results: {e}")
            return {}

    def sanitize_filename(self, filename: str) -> str:
        """Remove special characters from filename"""
        return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()

    def download_transcription(self, url: str, video_id: str, video_title: str) -> Dict:
        """
        Download transcription (manual subtitles preferred, auto-generated as fallback)

        Args:
            url: YouTube video URL
            video_id: Video ID
            video_title: Video title for filename

        Returns:
            Dictionary with transcription data and metadata
        """
        transcript_dir = self.output_dir / video_id 
        transcript_dir.mkdir(parents=True, exist_ok=True)

        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'en-US', 'en-GB'],  # Prioritize English
            'subtitlesformat': 'json3',  # Get detailed timing info
            'outtmpl': str(transcript_dir / f'transcripts.txt'),
            'quiet': False,
        }

        transcript_data = {
            'manual_subtitles': [],
            'auto_subtitles': [],
            'full_text': '',
            'format': None
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                # Try to get manual subtitles first
                if info.get('subtitles'):
                    for lang in ydl_opts['subtitleslangs']:
                        if lang in info['subtitles']:
                            print(f"Found manual subtitles in {lang}")
                            transcript_data['format'] = 'manual'
                            ydl.download([url])
                            break

                # Fallback to auto-generated
                elif info.get('automatic_captions'):
                    for lang in ydl_opts['subtitleslangs']:
                        if lang in info['automatic_captions']:
                            print(f"Using auto-generated captions in {lang}")
                            transcript_data['format'] = 'auto-generated'
                            ydl.download([url])
                            break

                # Parse the downloaded subtitle files
                for file in transcript_dir.glob('*.json3'):
                    with open(file, 'r', encoding='utf-8') as f:
                        subtitle_data = json.load(f)

                    # Extract text and timing
                    segments = []
                    full_text_parts = []

                    for event in subtitle_data.get('events', []):
                        if 'segs' in event:
                            text = ''.join(seg.get('utf8', '') for seg in event['segs'])
                            if text.strip():
                                segments.append({
                                    'start': event.get('tStartMs', 0) / 1000,
                                    'duration': event.get('dDurationMs', 0) / 1000,
                                    'text': text.strip()
                                })
                                full_text_parts.append(text.strip())

                    if transcript_data['format'] == 'manual':
                        transcript_data['manual_subtitles'] = segments
                    else:
                        transcript_data['auto_subtitles'] = segments

                    transcript_data['full_text'] = ' '.join(full_text_parts)

                    # Save cleaned transcript
                    transcript_file = transcript_dir / 'transcripts.txt'
                    with open(transcript_file, 'w', encoding='utf-8') as f:
                        f.write(transcript_data['full_text'])

                    print(f"Saved transcript to: {transcript_file}")

                    # Remove the JSON3 file after processing
                    file.unlink()

        except Exception as e:
            print(f"Error downloading transcription: {e}")
            transcript_data['error'] = str(e)

        return transcript_data

    def download_metadata(self, url: str) -> Dict:
        """
        Extract video metadata including description

        Args:
            url: YouTube video URL

        Returns:
            Dictionary with video metadata
        """
        ydl_opts = {
            'skip_download': True,
            'quiet': False,
        }

        metadata = {}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                metadata = {
                    'video_id': info.get('id'),
                    'title': info.get('title'),
                    'description': info.get('description'),
                    'uploader': info.get('uploader'),
                    'upload_date': info.get('upload_date'),
                    'duration': info.get('duration'),
                    'view_count': info.get('view_count'),
                    'like_count': info.get('like_count'),
                    'channel': info.get('channel'),
                    'channel_id': info.get('channel_id'),
                    'categories': info.get('categories'),
                    'tags': info.get('tags'),
                    'thumbnail': info.get('thumbnail'),
                }

                # Save metadata to JSON
                video_dir = self.output_dir / metadata['video_id']
                video_dir.mkdir(parents=True, exist_ok=True)

                metadata_file = video_dir / 'metadata.json'
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)

                # Save description to separate file
                description_file = video_dir / 'description.txt'
                with open(description_file, 'w', encoding='utf-8') as f:
                    f.write(metadata['description'] or '')

                print(f"Saved metadata to: {metadata_file}")
                print(f"Saved description to: {description_file}")

        except Exception as e:
            print(f"Error extracting metadata: {e}")
            metadata['error'] = str(e)

        return metadata

    def download_audio(self, url: str, video_id: str, video_title: str) -> Optional[str]:
        """
        Download audio in 16kHz mono format

        Args:
            url: YouTube video URL
            video_id: Video ID
            video_title: Video title for filename

        Returns:
            Path to downloaded audio file
        """
        audio_dir = self.output_dir / video_id
        audio_dir.mkdir(parents=True, exist_ok=True)

        output_template = str(audio_dir / f'audio.%(ext)s')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '0',
            }],
            'postprocessor_args': [
                '-ar', '16000',  # 16kHz sample rate
                '-ac', '1',       # Mono
            ],
            'prefer_ffmpeg': True,
            'keepvideo': False,
            'quiet': False,
        }

        audio_file = None

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                audio_file = audio_dir / 'audio.wav'
                print(f"Downloaded audio to: {audio_file}")

        except Exception as e:
            print(f"Error downloading audio: {e}")

        return str(audio_file) if audio_file else None

    def download_video(self, url: str, video_id: str, video_title: str) -> Optional[str]:
        """
        Download video in best quality

        Args:
            url: YouTube video URL
            video_id: Video ID
            video_title: Video title for filename

        Returns:
            Path to downloaded video file
        """
        video_dir = self.output_dir / video_id 
        video_dir.mkdir(parents=True, exist_ok=True)

        output_template = str(video_dir / f'video.%(ext)s')

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
            'quiet': False,
        }

        video_file = None

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_file = video_dir / f'{self.sanitize_filename(video_title)}.mp4'
                print(f"Downloaded video to: {video_file}")

        except Exception as e:
            print(f"Error downloading video: {e}")

        return str(video_file) if video_file else None

    def crawl(self, url: str) -> Dict:
        """
        Crawl all data from a YouTube video

        Args:
            url: YouTube video URL

        Returns:
            Dictionary with all crawled data and file paths
        """
        print(f"\n{'='*60}")
        print(f"Starting crawl for: {url}")
        print(f"{'='*60}\n")

        # First get metadata to get video ID and title
        print("Step 1: Extracting metadata...")
        metadata = self.download_metadata(url)

        if 'error' in metadata:
            return {'error': metadata['error']}

        video_id = metadata['video_id']
        video_title = metadata['title']

        results = {
            'url': url,
            'video_id': video_id,
            'title': video_title,
            'metadata': metadata,
        }

        # Download transcription
        print("\nStep 2: Downloading transcription...")
        transcription = self.download_transcription(url, video_id, video_title)
        results['transcription'] = transcription

        # Download audio
        print("\nStep 3: Downloading audio (16kHz mono)...")
        audio_path = self.download_audio(url, video_id, video_title)
        results['audio_path'] = audio_path

        # Download video
        print("\nStep 4: Downloading video...")
        video_path = self.download_video(url, video_id, video_title)
        results['video_path'] = video_path

        # Save complete results
        results_file = self.output_dir / video_id / 'crawl_results.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*60}")
        print(f"Crawl complete! Results saved to: {results_file}")
        print(f"{'='*60}\n")

        return results


def main():
    parser = argparse.ArgumentParser(
        description='Crawl YouTube video data including transcription, description, audio, and video'
    )
    parser.add_argument('url', nargs='?', help='YouTube video URL')
    parser.add_argument('-o', '--output', default='output', help='Output directory (default: output)')
    parser.add_argument('--skip-audio', action='store_true', help='Skip audio download')
    parser.add_argument('--skip-video', action='store_true', help='Skip video download')
    parser.add_argument('--skip-transcript', action='store_true', help='Skip transcription download')
    parser.add_argument('--add-diarization', nargs=2, metavar=('RESULTS_FILE', 'RTTM_FILE'),
                        help='Add speaker diarization to existing crawl results. Usage: --add-diarization <crawl_results.json> <audio.rttm>')

    args = parser.parse_args()

    crawler = YouTubeCrawler(output_dir=args.output)

    # Handle diarization mode
    if args.add_diarization:
        results_file, rttm_file = args.add_diarization
        print(f"Adding diarization from {rttm_file} to {results_file}...")
        crawler.add_diarization_to_results(results_file, rttm_file)
        return

    # Require URL for crawling mode
    if not args.url:
        parser.error('URL is required when not using --add-diarization')

    if args.skip_audio or args.skip_video or args.skip_transcript:
        # Custom crawl with skipped items
        metadata = crawler.download_metadata(args.url)
        video_id = metadata['video_id']
        video_title = metadata['title']

        if not args.skip_transcript:
            crawler.download_transcription(args.url, video_id, video_title)
        if not args.skip_audio:
            crawler.download_audio(args.url, video_id, video_title)
        if not args.skip_video:
            crawler.download_video(args.url, video_id, video_title)
    else:
        # Full crawl
        results = crawler.crawl(args.url)

        if 'error' not in results:
            print("\nCrawl Summary:")
            print(f"  Video ID: {results['video_id']}")
            print(f"  Title: {results['title']}")
            print(f"  Transcription: {results['transcription'].get('format', 'N/A')}")
            print(f"  Audio: {results.get('audio_path', 'N/A')}")
            print(f"  Video: {results.get('video_path', 'N/A')}")


if __name__ == '__main__':
    main()
