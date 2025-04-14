import requests
import re
import os
import tqdm
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
import json
import sys
from util import get_title
DUR_RATIO = 0.7

def replace_print(text):
    sys.stdout.write('\r' + str(text))
    sys.stdout.flush()

def main(name_file, downloaded_file, language, download_folder, index):
    ytt_api = YouTubeTranscriptApi()
    
    # Create links directory if it doesn't exist
    os.makedirs("links", exist_ok=True)
    
    # Create a single link list file
    with open("links/link_list.txt", "w") as f:
        pass
    
    # Read names from the specified file
    with open(name_file, "r") as f:
        lst = f.readlines()
    lst = [i.strip() for i in lst]
    
    # Create download folders if they don't exist
    os.makedirs(f"{download_folder}/downloaded_subtitle", exist_ok=True)
    
    # Read downloaded videos
    downloaded_subtitle = os.listdir(f"{download_folder}/downloaded_subtitle")
    downloaded_subtitle = [i.rstrip(".jsonl") for i in downloaded_subtitle]
    
    regex = r"(?<=watch\?v=)[\w]+(?=\")"
    
    for j in tqdm.tqdm(lst):
        match_all = []
        for i in range(0, 5):  # search first n pages
            URL = (
                f"https://www.youtube.com/results?search_query={j}"
                "&sp=EgQQASgB&page=" + str(i)
            )
            try:
                page = requests.get(URL)
                a = page.text
                match = re.findall(regex, a)
                match_all += match
            except Exception as e:
                print(f"Error fetching search results: {e}")
                continue

        match_all = list(set(match_all))
        match_all_real = []
        duration_lst = []
        sub_duration_lst = []
        meta_lst_all = []
        
        for u in match_all:
            if u not in downloaded_subtitle:
                try:
                    transcript_list = ytt_api.list(u)
                    if language in transcript_list._manually_created_transcripts:
                        sub_dur = 0
                        # Use the language parameter passed to the function
                        transcript = transcript_list.find_manually_created_transcript([language])
                        e = transcript.fetch()
                        
                        meta_lst = []
                        for snip in e.snippets:
                            d = dict()
                            d["text"] = snip.text
                            d["start"] = snip.start
                            d["duration"] = snip.duration
                            sub_dur += snip.duration
                            meta_lst.append(d)
                        video_dur = e.snippets[-1].start + e.snippets[-1].duration

                        if len(e) > 10 and sub_dur > video_dur * DUR_RATIO:
                            meta_lst_all.append(meta_lst)
                            duration_lst.append(video_dur)
                            match_all_real.append(u)
                            sub_duration_lst.append(sub_dur)
                except Exception as e:
                    print(f"Error processing video {u}: {e}")
                    continue
            else:
                replace_print("already exist: " + u)

        for t, dur, sub_dur, meta_data in zip(match_all_real, duration_lst, sub_duration_lst, meta_lst_all):
            if t in downloaded_subtitle:
                pass
            else:
                print("downloading: " + t)
                downloaded_subtitle.append(t)
                link = f"https://www.youtube.com/watch?v={t}"
                with open("links/link_list.txt", "a") as f:
                    f.write(f"{link}\n")
                title=get_title(t)
                with open(f"{download_folder}/downloaded_subtitle/{t}.jsonl", "w", encoding="utf-8") as f:
                    final_dict = {"language": language, "phrase_index": index, "id": t,"title":title, "subtitles": meta_data}
                    json.dump(final_dict, f, indent=4, ensure_ascii=False)

    print("\nFinished processing all search terms")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="YouTube Crawler")
    parser.add_argument("name_file", help="Path to the file containing names to search")
    parser.add_argument("--downloaded", 
                        default="downloaded.txt", 
                        help="Path to the file tracking downloaded videos")
    parser.add_argument("--language", 
                        default="vi", 
                        help="Language code for transcripts (default: vi)")
    parser.add_argument("--download_folder", 
                        default="../downloaded_subtitle", 
                        help="download_folder")
    parser.add_argument("--index", 
                        default="1", 
                        help="phrase index")
    
    # Parse arguments
    args = parser.parse_args()

    # Call main with parsed arguments
    main(args.name_file, args.downloaded, args.language, args.download_folder, args.index)
