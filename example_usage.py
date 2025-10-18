#!/usr/bin/env python3
"""
Example usage of the YouTube crawler
"""

from youtube_crawler import YouTubeCrawler

# Example YouTube URLs
example_urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Replace with your URL
]

def main():
    # Initialize crawler with output directory
    crawler = YouTubeCrawler(output_dir="youtube_data")

    # Crawl a single video
    url = input("Enter YouTube video URL: ").strip()

    if not url:
        print("Using example URL for demonstration...")
        url = example_urls[0]

    # Full crawl - gets everything
    results = crawler.crawl(url)

    if 'error' in results:
        print(f"Error: {results['error']}")
        return

    # Access the results
    print("\n" + "="*60)
    print("CRAWL RESULTS")
    print("="*60)

    print(f"\nVideo Information:")
    print(f"  ID: {results['video_id']}")
    print(f"  Title: {results['title']}")
    print(f"  Duration: {results['metadata'].get('duration')} seconds")
    print(f"  Uploader: {results['metadata'].get('uploader')}")

    print(f"\nTranscription:")
    if results['transcription'].get('full_text'):
        print(f"  Format: {results['transcription']['format']}")
        print(f"  Length: {len(results['transcription']['full_text'])} characters")
        print(f"  Preview: {results['transcription']['full_text'][:200]}...")
    else:
        print("  No transcription available")

    print(f"\nFiles Downloaded:")
    print(f"  Audio (16kHz mono): {results.get('audio_path')}")
    print(f"  Video: {results.get('video_path')}")

    print("\n" + "="*60)


if __name__ == '__main__':
    main()
