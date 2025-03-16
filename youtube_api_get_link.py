# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
api_key="AIzaSyB7pGUOwlnJudlluLBcF8HwYWzl8E6eE6A"
youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=api_key)

import json
def get_id_list(keyword):
        response = youtube.search().list(
                part="id",
                order='date',
                type='video',
                videoCaption='closedCaption',
                maxResults=1500,
                pageToken=None,
                q=keyword,
                ).execute()
        b=response["items"]
        c=[i["id"]["videoId"] for i in b]
        # d=[i["snippet"]["title"] for i in b]
        return c

import requests
import re
import os
import tqdm
import random
from youtube_transcript_api import YouTubeTranscriptApi


from multiprocessing import Process

def get_url(v):
    with open("link_list"+str(v)+".txt", "w") as f:
        pass
    with open("/home3/cuongld/asr-training/data/vocab/word_list_miss_indomain.txt", "r") as f:
        lst=f.readlines()
    lst=[i.strip() for i in lst]
    length=len(lst)
    lst=lst[int(v*length/6):int((v+1)*length/6)]
    with open("/home/khanhnd/youtube_crawler/KTSpeechCrawler/vi-downloaded.txt","r") as f:
        all=f.readlines()
        all=[i.strip().split()[-1] for i in all]
    for j in tqdm.tqdm(lst):
        print("searching for ", j)
        match_all=get_id_list(j)
        
        match_all=list(set(match_all))
        
        match_all_real=[]
        for u in match_all:
            if u not in all:
                try:
                    transcript_list = YouTubeTranscriptApi.list_transcripts(u)

                    transcript = transcript_list.find_manually_created_transcript(["vi"])
                    e=transcript.fetch()
                    if len(e)>10:
                        match_all_real.append(u)
                    else:
                        pass

                except Exception:
                    pass

        print("number of vid found: ", len(match_all_real))    
        print("len", len(match_all_real))
        if len(match_all_real)>=30:
            l=random.sample(match_all_real, 30)
        else:
            print("NOT_ENOUGH")
            l=match_all_real
        for t in l:
            if t in all:
                print(t)
            if t not in all:
                all.append(t)
                print("get")
                link="https://www.youtube.com/watch?v="+t
                with open("link_list"+str(v)+".txt", "a") as f:
                    f.write(link+"\n")

# Create new threads
def main():

    p0 = Process(target=get_url, args=(0, ))
    p0.start()

    p1 = Process(target=get_url, args=(1, ))
    p1.start()
    # p1.join()

    p2 = Process(target=get_url, args=(2, ))
    p2.start()
    # p2.join()

    p3 = Process(target=get_url, args=(3, ))
    p3.start()
    # p3.join()

    p4 = Process(target=get_url, args=(4, ))
    p4.start()

    p5= Process(target=get_url, args=(5, ))
    p5.start()


    p0.join()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()

    print('finished main') 

if __name__ == '__main__':
    
    main()