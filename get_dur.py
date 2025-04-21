import glob
import json
import os
import librosa
from tqdm import tqdm
lan="ja"
subtitle_lst=glob.glob("/Users/khanh/dev/crawler/database/downloaded_subtitle/*")
audio_existed=[i[:-4] for i in os.listdir("/Users/khanh/dev/crawler/database/downloaded_audio/")]
count=0
count_audio=0
hehe=0
for i in tqdm(subtitle_lst):
    metadata=json.load(open(i))
    if metadata["language"] == lan and metadata["id"] in  audio_existed:
        count_audio+=librosa.get_duration(path="/Users/khanh/dev/crawler/database/downloaded_audio/"+metadata["id"]+".wav")
        hehe+=1
        for v in metadata["subtitles"]:
            count+=v["duration"]
    
print(count/3600)
print(count_audio/3600)
        