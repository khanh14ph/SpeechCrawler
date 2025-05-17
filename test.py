from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
transcript_list = ytt_api.list("TVh6En6eHoo")

transcript=transcript_list.find_manually_created_transcript(["ko"])
for i in range(10):
    print(i)
    transcript.fetch()
