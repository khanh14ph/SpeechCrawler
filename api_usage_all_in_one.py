#!/usr/bin/env python3
"""
YouTube Crawler - All-in-One API Usage Example
This script demonstrates all major features of the YouTube crawler in a single file.
"""

import sys
sys.path.insert(0, '/Users/khanh/dev/crawler/yt-dlp')

from youtube_crawler import YouTubeCrawler
import json
from pathlib import Path


def example_1_basic_crawl():
    """Example 1: Basic video crawl - downloads everything"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Full Crawl")
    print("="*80)

    crawler = YouTubeCrawler(output_dir="output")

    # Replace with your YouTube URL
    url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

    results = crawler.crawl(url)

    if 'error' not in results:
        print(f"\nSuccessfully crawled: {results['title']}")
        print(f"  Video ID: {results['video_id']}")
        print(f"  Transcription format: {results['transcription'].get('format')}")
        print(f"  Audio file: {results.get('audio_path')}")
        print(f"  Video file: {results.get('video_path')}")

    return results


def example_2_metadata_only():
    """Example 2: Download only metadata and description"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Metadata Only")
    print("="*80)

    crawler = YouTubeCrawler(output_dir="output")
    url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

    metadata = crawler.download_metadata(url)

    print(f"\nVideo Metadata:")
    print(f"  Title: {metadata.get('title')}")
    print(f"  Channel: {metadata.get('channel')}")
    print(f"  Duration: {metadata.get('duration')} seconds")
    print(f"  Views: {metadata.get('view_count')}")
    print(f"  Upload Date: {metadata.get('upload_date')}")
    print(f"  Categories: {metadata.get('categories')}")
    print(f"  Tags: {metadata.get('tags')[:5] if metadata.get('tags') else 'None'}...")
    print(f"\nDescription preview:")
    print(f"  {metadata.get('description', '')[:200]}...")

    return metadata


def example_3_transcription_only():
    """Example 3: Download only transcription/subtitles"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Transcription Only")
    print("="*80)

    crawler = YouTubeCrawler(output_dir="output")
    url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

    # Get video ID first
    metadata = crawler.download_metadata(url)
    video_id = metadata['video_id']
    video_title = metadata['title']

    transcription = crawler.download_transcription(url, video_id, video_title)

    print(f"\nTranscription Results:")
    print(f"  Format: {transcription.get('format')}")
    print(f"  Full text length: {len(transcription.get('full_text', ''))} characters")

    # Access manual subtitles with timing
    if transcription.get('manual_subtitles'):
        print(f"\n  Manual subtitles: {len(transcription['manual_subtitles'])} segments")
        print(f"  First 3 segments:")
        for seg in transcription['manual_subtitles'][:3]:
            print(f"    [{seg['start']:.2f}s - {seg['start'] + seg['duration']:.2f}s]: {seg['text']}")

    # Access auto-generated subtitles with timing
    if transcription.get('auto_subtitles'):
        print(f"\n  Auto subtitles: {len(transcription['auto_subtitles'])} segments")
        print(f"  First 3 segments:")
        for seg in transcription['auto_subtitles'][:3]:
            print(f"    [{seg['start']:.2f}s - {seg['start'] + seg['duration']:.2f}s]: {seg['text']}")

    return transcription


def example_4_audio_only():
    """Example 4: Download only audio (16kHz mono WAV)"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Audio Download Only")
    print("="*80)

    crawler = YouTubeCrawler(output_dir="output")
    url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

    metadata = crawler.download_metadata(url)
    video_id = metadata['video_id']
    video_title = metadata['title']

    audio_path = crawler.download_audio(url, video_id, video_title)

    print(f"\nAudio downloaded to: {audio_path}")
    print(f"  Format: 16kHz mono WAV")

    # Check file size
    if audio_path:
        file_size = Path(audio_path).stat().st_size / (1024 * 1024)  # MB
        print(f"  File size: {file_size:.2f} MB")

    return audio_path


def example_5_video_only():
    """Example 5: Download only video"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Video Download Only")
    print("="*80)

    crawler = YouTubeCrawler(output_dir="output")
    url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

    metadata = crawler.download_metadata(url)
    video_id = metadata['video_id']
    video_title = metadata['title']

    video_path = crawler.download_video(url, video_id, video_title)

    print(f"\nVideo downloaded to: {video_path}")
    print(f"  Format: Best quality MP4")

    if video_path:
        file_size = Path(video_path).stat().st_size / (1024 * 1024)  # MB
        print(f"  File size: {file_size:.2f} MB")

    return video_path


def example_6_custom_selection():
    """Example 6: Download custom selection (metadata + transcription + audio)"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Custom Selection (No Video)")
    print("="*80)

    crawler = YouTubeCrawler(output_dir="output")
    url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

    # Step 1: Get metadata
    print("\nStep 1: Getting metadata...")
    metadata = crawler.download_metadata(url)
    video_id = metadata['video_id']
    video_title = metadata['title']

    # Step 2: Get transcription
    print("\nStep 2: Getting transcription...")
    transcription = crawler.download_transcription(url, video_id, video_title)

    # Step 3: Get audio (skip video)
    print("\nStep 3: Getting audio...")
    audio_path = crawler.download_audio(url, video_id, video_title)

    # Build custom results
    results = {
        'url': url,
        'video_id': video_id,
        'title': video_title,
        'metadata': metadata,
        'transcription': transcription,
        'audio_path': audio_path,
        'video_path': None  # Skipped
    }

    print(f"\nCustom crawl complete!")
    print(f"  Downloaded: Metadata + Transcription + Audio")
    print(f"  Skipped: Video")

    return results


def example_7_batch_crawl():
    """Example 7: Batch crawl multiple videos"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Batch Crawl Multiple Videos")
    print("="*80)

    crawler = YouTubeCrawler(output_dir="output")

    urls = [
        "https://www.youtube.com/watch?v=VIDEO_ID_1",
        "https://www.youtube.com/watch?v=VIDEO_ID_2",
        "https://www.youtube.com/watch?v=VIDEO_ID_3",
    ]

    all_results = []

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Processing: {url}")
        try:
            results = crawler.crawl(url)
            all_results.append(results)
            print(f"  Success: {results['title']}")
        except Exception as e:
            print(f"  Error: {e}")
            all_results.append({'url': url, 'error': str(e)})

    print(f"\nBatch crawl complete! Processed {len(all_results)} videos")

    return all_results


def example_8_access_results():
    """Example 8: Access and analyze saved results"""
    print("\n" + "="*80)
    print("EXAMPLE 8: Access Previously Crawled Results")
    print("="*80)

    # Load results from a previous crawl
    results_file = Path("output/VIDEO_ID/crawl_results.json")

    if not results_file.exists():
        print(f"\nResults file not found: {results_file}")
        print("Run a crawl first!")
        return None

    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    print(f"\nLoaded results for: {results['title']}")
    print(f"  Video ID: {results['video_id']}")

    # Access transcription segments
    if results['transcription'].get('manual_subtitles'):
        segments = results['transcription']['manual_subtitles']
        print(f"\n  Total transcript segments: {len(segments)}")

        # Find segments mentioning a keyword
        keyword = "example"
        matching_segments = [s for s in segments if keyword.lower() in s['text'].lower()]
        print(f"  Segments containing '{keyword}': {len(matching_segments)}")

        for seg in matching_segments[:3]:
            print(f"    [{seg['start']:.2f}s]: {seg['text']}")

    # Access metadata
    print(f"\n  Duration: {results['metadata']['duration']}s")
    print(f"  Views: {results['metadata']['view_count']}")

    return results


def example_9_speaker_diarization():
    """Example 9: Add speaker diarization to existing results"""
    print("\n" + "="*80)
    print("EXAMPLE 9: Add Speaker Diarization")
    print("="*80)

    crawler = YouTubeCrawler(output_dir="output")

    # Paths to your files
    results_file = "output/VIDEO_ID/crawl_results.json"
    rttm_file = "output/VIDEO_ID/audio.rttm"

    # Check if files exist
    if not Path(results_file).exists():
        print(f"\nResults file not found: {results_file}")
        print("Run a crawl first!")
        return None

    if not Path(rttm_file).exists():
        print(f"\nRTTM file not found: {rttm_file}")
        print("Generate speaker diarization RTTM file first!")
        print("You can use pyannote.audio or other diarization tools")
        return None

    # Add diarization information
    updated_results = crawler.add_diarization_to_results(results_file, rttm_file)

    # Access updated transcripts with speaker IDs
    if updated_results['transcription'].get('auto_subtitles'):
        print("\nTranscript segments with speakers:")
        for seg in updated_results['transcription']['auto_subtitles'][:5]:
            speaker = seg.get('speaker_id', 'UNKNOWN')
            print(f"  [{seg['start']:.2f}s] {speaker}: {seg['text']}")

    return updated_results


def example_10_analyze_transcript():
    """Example 10: Analyze transcript content"""
    print("\n" + "="*80)
    print("EXAMPLE 10: Transcript Analysis")
    print("="*80)

    crawler = YouTubeCrawler(output_dir="output")
    url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

    metadata = crawler.download_metadata(url)
    video_id = metadata['video_id']
    video_title = metadata['title']

    transcription = crawler.download_transcription(url, video_id, video_title)

    if transcription.get('auto_subtitles'):
        segments = transcription['auto_subtitles']

        # Calculate speaking statistics
        total_segments = len(segments)
        total_duration = sum(seg['duration'] for seg in segments)
        avg_segment_length = total_duration / total_segments if total_segments > 0 else 0

        print(f"\nTranscript Statistics:")
        print(f"  Total segments: {total_segments}")
        print(f"  Total speaking time: {total_duration:.2f} seconds")
        print(f"  Average segment length: {avg_segment_length:.2f} seconds")

        # Word count
        full_text = transcription.get('full_text', '')
        word_count = len(full_text.split())
        words_per_minute = (word_count / total_duration) * 60 if total_duration > 0 else 0

        print(f"  Total words: {word_count}")
        print(f"  Speaking rate: {words_per_minute:.1f} words/minute")

        # Find longest pause
        pauses = []
        for i in range(len(segments) - 1):
            current_end = segments[i]['start'] + segments[i]['duration']
            next_start = segments[i + 1]['start']
            pause = next_start - current_end
            if pause > 0:
                pauses.append(pause)

        if pauses:
            print(f"  Average pause: {sum(pauses) / len(pauses):.2f} seconds")
            print(f"  Longest pause: {max(pauses):.2f} seconds")

    return transcription


def main():
    """Run all examples (or choose specific ones)"""
    print("YouTube Crawler - All-in-One API Usage Examples")
    print("="*80)

    # Uncomment the examples you want to run:

    # Basic usage
    # example_1_basic_crawl()

    # Individual components
    # example_2_metadata_only()
    # example_3_transcription_only()
    # example_4_audio_only()
    # example_5_video_only()

    # Custom workflows
    # example_6_custom_selection()
    # example_7_batch_crawl()

    # Advanced analysis
    # example_8_access_results()
    # example_9_speaker_diarization()
    # example_10_analyze_transcript()

    print("\n" + "="*80)
    print("USAGE GUIDE")
    print("="*80)
    print("""
To use this script:

1. Edit the script and replace 'YOUR_VIDEO_ID' with actual YouTube video URLs
2. Uncomment the example(s) you want to run in the main() function
3. Run the script: python api_usage_all_in_one.py

Available Examples:
  1. Basic full crawl - Downloads everything
  2. Metadata only - Get video info and description
  3. Transcription only - Get subtitles with timing
  4. Audio only - Download 16kHz mono WAV
  5. Video only - Download best quality video
  6. Custom selection - Pick what you need
  7. Batch crawl - Process multiple videos
  8. Access results - Load and analyze saved data
  9. Speaker diarization - Add speaker labels to transcripts
  10. Transcript analysis - Calculate statistics

For more details, see the function docstrings in this file.
    """)


if __name__ == '__main__':
    main()
