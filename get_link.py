import requests
import re
import os
import tqdm
import random
from youtube_transcript_api import YouTubeTranscriptApi


from multiprocessing import Process

# /home3/cuongld/asr-training/data/vocab/word_list_miss_indomain.txt
def get_url(v):
    with open("link_list" + str(v) + ".txt", "w") as f:
        pass
    with open(
        "/home4/khanhnd/youtube_crawler/KTSpeechCrawler/name.txt", "r"
    ) as f:
        lst = f.readlines()
    lst = [i.strip() for i in lst]
    length = len(lst)
    lst = lst[int(v * length / 6) : int((v + 1) * length / 6)]
    regex = r"(?<=watch\?v=)[\w]+(?=\")"
    with open("/home4/khanhnd/youtube_crawler/KTSpeechCrawler/vi-downloaded.txt", "r") as f:
        all = f.readlines()
        all = [i.strip().split()[-1] for i in all]
    for j in tqdm.tqdm(lst):
        print("searching for ", j)
        match_all = []
        for i in range(0, 30):  # search first n pages

            URL = (
                "https://www.youtube.com/results?search_query="
                + j
                + "&sp=EgQQASgB&page="
                + str(i)
            )
            page = requests.get(URL)
            a = page.text
            match = re.findall(regex, a)

            match_all += match

        match_all = list(set(match_all))

        match_all_real = []
        for u in match_all:
            if u not in all:
                try:
                    transcript_list = YouTubeTranscriptApi.list_transcripts(u)

                    transcript = transcript_list.find_manually_created_transcript(
                        ["vi"]
                    )
                    e = transcript.fetch()
                    if len(e) > 10:
                        match_all_real.append(u)
                    else:
                        pass

                except Exception:
                    pass

        print("number of vid found: ", len(match_all_real))
        print("len", len(match_all_real))
        if len(match_all_real) >= 30:
            l = random.sample(match_all_real, 30)
        else:
            print("NOT_ENOUGH")
            l = match_all_real
        for t in l:
            if t in all:
                print(t)
            if t not in all:
                all.append(t)
                print("get")
                link = "https://www.youtube.com/watch?v=" + t
                with open("link_list" + str(v) + ".txt", "a") as f:
                    f.write(link + "\n")


# Create new threads
def main():

    p0 = Process(target=get_url, args=(0,))
    p0.start()

    p1 = Process(target=get_url, args=(1,))
    p1.start()
    # p1.join()

    p2 = Process(target=get_url, args=(2,))
    p2.start()
    # p2.join()

    p3 = Process(target=get_url, args=(3,))
    p3.start()
    # p3.join()

    p4 = Process(target=get_url, args=(4,))
    p4.start()

    p5 = Process(target=get_url, args=(5,))
    p5.start()

    p0.join()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()

    print("finished main")


if __name__ == "__main__":

    main()
