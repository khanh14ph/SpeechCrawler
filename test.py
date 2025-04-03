from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
transcript_list = ytt_api.list("WQA0XuyInsc")
transcript=transcript_list.find_manually_created_transcript(["vi"])
e = transcript.fetch()
lst=[]
for snip in e.snippets:
    d=dict()
    d["text"]=snip.text
    d["start"]=snip.start
    d["duration"]=snip.duration
    lst.append(d)
print(lst)
    
