import glob
import sys
import json
# Get filename from command line arguments
if len(sys.argv) > 1:
    folder_subtitle = sys.argv[1]
    folder_audio = sys.argv[2]
    language=sys.argv[3]
else:
    print("Error: Please provide a filename as a command line argument")
    sys.exit(1)
import os
subtitle_lst=os.listdir(f"{folder_subtitle}")

audio_lst=os.listdir(f"{folder_audio}")
audio_lst=[i[:-4] for i in audio_lst]
lst=[]
attempted_to_download=open("downloaded_urls.txt","r",encoding="utf-8").read().splitlines()
attempted_to_download=[i.split()[-1] for i in attempted_to_download] 
for i in subtitle_lst:
    d=json.load(open(f"{folder_subtitle}/{i}"))
    if d["language"]==language and d["id"] not in audio_lst and d["id"] not in attempted_to_download:
        lst.append(i[:-6])
print("need to download: ",len(lst))
with open("temp_url.txt","w",encoding="utf-8") as f:
    for i in lst:
        f.write(f"https://www.youtube.com/watch?v={i}\n")
