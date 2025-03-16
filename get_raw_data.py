import os
import glob
path="/home/khanhnd/youtube_crawler/KTSpeechCrawler/final_results/txt/*"
lst=[]
for file in glob.glob(path, recursive=True):
    lst.append(file)
txt_lst=[]
for vid in lst:
    for file in glob.glob(vid+"/*"):
        txt_lst.append(file)
wav_lst=[i[:60]+"wav"+i[63:-3]+"wav" for i in txt_lst]
# raw_data_path=["/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_0.txt"]
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_1.txt")
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_2.txt")
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_3.txt")
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_4.txt")
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_5.txt")
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_6.txt")
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_7.txt")
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_8.txt")
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_9.txt")
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_10.txt")
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_11.txt")
# raw_data_path.append("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_12.txt")
import glob
import tqdm
path="/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_*"
raw_data_path=[]

for file in glob.glob(path, recursive=True):
    raw_data_path.append(file)
index=[int(i.split("/")[-1].split("_")[-1].split(".")[0]) for i in raw_data_path]    
import pandas as pd
existed=[]
for i in raw_data_path:
    with open(i,"r") as f:
        t=f.readlines()
        for i in t[1:]:
            p=i.strip().split(",")[0]
            existed.append(p)
import tqdm
import tqdm
not_existed_wav=list(set(wav_lst) - set(existed))
not_existed_txt=[i[:60]+"txt"+i[63:-3]+"txt" for i in not_existed_wav]
import tqdm
print(len(not_existed_txt))
print(str(max(index)+1))
with open("/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/raw_data_"+str(max(index)+1)+".txt", "w") as f:
    lines="wav_path, subtitle\n"
    index=0
    for wav in tqdm.tqdm(not_existed_wav):
        txt=not_existed_txt[index]
        try:
            with open(txt, "r") as f1:
                l=f1.readlines()[0].strip()
            lines=lines+wav+","+l+"\n"
        except:
            print("no_sub")
        index+=1
    f.write(lines)
