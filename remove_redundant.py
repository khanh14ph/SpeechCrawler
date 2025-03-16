import librosa
s=0
good_s=0
import glob
import tqdm
path="/home/khanhnd/youtube_crawler/KTSpeechCrawler/crawler/clean_data_*"
lst=[]
for file in glob.glob(path, recursive=True):
    lst.append(file)
wav_lst=[]
for i in lst:
    with open(i,"r") as f:

        t=f.readlines()[1:]
        for v in t[1:]:
            score=v.strip().split(",")[-1]
            p=v.strip().split(",")[0]
            wav_lst.append(p)
print(len(wav_lst))
path="/home/khanhnd/youtube_crawler/KTSpeechCrawler/final_results/wav/*"
lst=[]
for file in glob.glob(path, recursive=True):
    lst.append(file)
wav_lst1=[]
for vid in lst:
    for file in glob.glob(vid+"/*"):
        wav_lst1.append(file)

redundant=list(set(wav_lst1)-set(wav_lst))
print(len(redundant))
import os
import tqdm
for i in tqdm.tqdm(redundant):
    os.remove(i)
            
