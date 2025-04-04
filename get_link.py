import requests
import re
import os
import tqdm
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from multiprocessing import Process
import json
def get_url(v, name_file, downloaded_file, language,download_subtitle_folder,index):
    ytt_api = YouTubeTranscriptApi(cookie_path='cookies.txt')
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
        meta_lst_all=[]
        for u in match_all:
            if u not in all_lst:
                    
                    transcript_list = ytt_api.list(u)
                    if language in transcript_list._manually_created_transcripts:
                        sub_dur = 0
                    # Use the language parameter passed to the function
                        transcript = transcript_list.find_manually_created_transcript([language])
                        e = transcript.fetch()
                        
                        meta_lst=[]
                        for snip in e.snippets:
                            d=dict()
                            d["text"]=snip.text
                            d["start"]=snip.start
                            d["duration"]=snip.duration
                            sub_dur+= snip.duration
                            meta_lst.append(d)
                        

                        if len(e) > 10:
                            meta_lst_all.append(meta_lst)
                            duration_lst.append(e.snippets[-1].start+e.snippets[-1].duration)

                            match_all_real.append(u)
                            sub_duration_lst.append(sub_dur)
                        else:
                            pass



        for t, dur, sub_dur,meta_lst in zip(match_all_real, duration_lst, sub_duration_lst,match_all_real):
            if t in all_lst:
                print(t)
            if t not in all_lst:
                # all_lst.append(t)
                link = f"https://www.youtube.com/watch?v={t}"
                with open(f"links/link_list{v}.txt", "a") as f:
                    f.write(f"{link}\n")
                with open(f"{download_subtitle_folder}/{language}/{t}.jsonl","w",encoding="utf-8") as f:
                    final_dict={"phrase_index":index,"subtitles":meta_lst}
                    json.dump(final_dict, f, indent=4,ensure_ascii=False)

def main(name_file, downloaded_file, language,download_subtitle_folder):
    processes = []
    for i in range(6):
        p = Process(target=get_url, args=(i, name_file, downloaded_file, language,download_subtitle_folder,index))
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
                        default="downloaded.txt", 
                        help="Path to the file tracking downloaded videos")
    parser.add_argument("--language", 
                        default="vi", 
                        help="Language code for transcripts (default: vi)")
    parser.add_argument("--download_subtitle_folder", 
                        default="../downloaded_subtitle", 
                        help="download_subtitle_folder")
    parser.add_argument("--index", 
                        default="1", 
                        help="phrase index")
    
    # Parse arguments
    args = parser.parse_args()

    # Call main with parsed arguments
    main(args.name_file, args.downloaded, args.language,args.download_subtitle_folder,args.index)