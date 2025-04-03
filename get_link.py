import requests
import re
import os
import tqdm
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from multiprocessing import Process

def get_url(v, name_file, downloaded_file, language):
    with open(f"links/link_list{v}.txt", "w") as f:
        pass
    
    # Read names from the specified file
    with open(name_file, "r") as f:
        lst = f.readlines()
    lst = [i.strip() for i in lst]
    length = len(lst)
    lst = lst[int(v * length / 6) : int((v + 1) * length / 6)]
    
    regex = r"(?<=watch\?v=)[\w]+(?=\")"
    
    # Read downloaded videos from the specified file
    with open(downloaded_file, "r") as f:
        all_lst = f.readlines()
        all_lst = [i.strip().split()[-1] for i in all_lst]
    
    for j in tqdm.tqdm(lst):
        print("searching for ", j)
        match_all = []
        for i in range(0, 20):  # search first n pages
            URL = (
                f"https://www.youtube.com/results?search_query={j}"
                "&sp=EgQQASgB&page=" + str(i)
            )
            page = requests.get(URL)
            a = page.text
            match = re.findall(regex, a)

            match_all += match

        match_all = list(set(match_all))
        match_all_real = []
        duration_lst = []
        sub_duration_lst = []
        for u in match_all:
            if u not in all_lst:
                try:
                    sub_dur = 0
                    transcript_list = YouTubeTranscriptApi.list_transcripts(u)
                    
                    # Use the language parameter passed to the function
                    transcript = transcript_list.find_manually_created_transcript([language])
                    
                    e = transcript.fetch()
                    for v in e:
                        sub_dur = sub_dur + v["duration"]
                    sub_duration_lst.append(sub_dur)
                    if len(e) > 10:
                        duration_lst.append(e[-1]["start"])
                        match_all_real.append(u)
                    else:
                        pass

                except Exception as ex:
                    pass

        print("number of vid found: ", len(match_all_real))

        for t, dur, sub_dur in zip(match_all_real, duration_lst, sub_duration_lst):
            if t in all_lst:
                print(t)
            if t not in all_lst:
                all_lst.append(t)
                print("get")
                link = f"https://www.youtube.com/watch?v={t}"
                with open(f"link_list{v}.txt", "a") as f:
                    f.write(f"{link}\t{sub_dur}\t{dur}\n")

def main(name_file, downloaded_file, language):
    processes = []
    for i in range(6):
        p = Process(target=get_url, args=(i, name_file, downloaded_file, language))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("finished main")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="YouTube Crawler")
    parser.add_argument("name_file", help="Path to the file containing names to search")
    parser.add_argument("--downloaded", 
                        default="/home4/khanhnd/youtube_crawler/SpeechCrawler/downloaded.txt", 
                        help="Path to the file tracking downloaded videos")
    parser.add_argument("--language", 
                        default="vi", 
                        help="Language code for transcripts (default: vi)")
    
    # Parse arguments
    args = parser.parse_args()

    # Call main with parsed arguments
    main(args.name_file, args.downloaded, args.language)