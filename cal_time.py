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
            score=float(v.strip().split(",")[-1])
            p=v.strip().split(",")[0]
            wav_lst.append((p,score))
s=0
good_s=0
for path,score in tqdm.tqdm(wav_lst):
        l=librosa.get_duration(filename=path)
        s+=l
        if score>0.85:
            good_s+=l

print("all_total_time in hours",s/3600)
print("good_total_time in hours",good_s/3600)
