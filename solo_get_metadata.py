import os
import json
import argparse
import sys
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import requests
import re

def get_title(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.get(url)
        html = response.text
        title_match = re.search(r'<title>(.*?)</title>', html)
        if title_match:
            title = title_match.group(1).replace(" - YouTube", "").strip()
            return title
        return "Unknown Title"
    except Exception as e:
        print(f"⚠️ Failed to fetch title for {video_id}: {e}")
        return "Unknown Title"

def main(video_id, language, download_folder, phrase_index):
    # os.makedirs(f"{download_folder}/downloaded_subtitle", exist_ok=True)

    print(f"🔍 Processing video ID: {video_id} | Language: {language}")

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        if language in transcript_list._manually_created_transcripts:
            transcript = transcript_list.find_transcript([language])
            entries = transcript.fetch()

            meta_lst = []
            sub_duration = 0.0

            for snip in entries:
                meta_lst.append({
                    "text": snip.text,
                    "start": snip.start,
                    "duration": snip.duration
                })
                sub_duration += snip.duration

            if len(meta_lst) < 10:
                print("⚠️ Subtitle too short (<10 segments), skipping.")
                return

            video_duration = meta_lst[-1]["start"] + meta_lst[-1]["duration"]
            if sub_duration < 0.7 * video_duration:
                print("⚠️ Subtitle duration too short relative to video.")
                return

            title = get_title(video_id)
            save_path = f"{download_folder}/es/{video_id}.jsonl"

            final_dict = {
                "language": language,
                "phrase_index": phrase_index,
                "id": video_id,
                "title": title,
                "subtitles": meta_lst
            }

            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(final_dict, f, indent=4, ensure_ascii=False)

            print(f"✅ Saved {video_id}.jsonl | phrase_index: \"{phrase_index}\"")
        else:
            print(f"❌ No manually created subtitle found for language: {language}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="YouTube single video subtitle crawler")
    # parser.add_argument("--video_id", required=True, help="YouTube video ID (e.g., qLFefJL4YAE)")
    # parser.add_argument("--language", required=True, help="Subtitle language (e.g., pt, en, vi)")
    # parser.add_argument("--download_folder", default="./data", help="Output directory")
    # parser.add_argument("--phrase_index", required=True, help="Manual phrase index (e.g., '1')")

    # args = parser.parse_args()
    # main(args.video_id, args.language, args.download_folder, args.phrase_index)
    video_id = "uOXhwhjIOQ0"
    language = "es-419"
    phrase_index = "20"
    download_folder = "<DOWNLOAD_FOLDER"

    main(video_id, language, download_folder, phrase_index)
