from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
transcript_list = ytt_api.list("u76K3F-LZ0s")

transcript=transcript_list.find_manually_created_transcript(["zh-TW"])
e = transcript.fetch()

    
print(e)