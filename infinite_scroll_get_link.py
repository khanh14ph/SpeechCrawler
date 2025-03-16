import subprocess
import json
import datetime
def search(query, max_results=5):
    # Parameters for calling yt-dlp
    command = [
            'yt-dlp',
            'ytsearch{}:{}'.format(max_results, query),
            '--dump-json', 
            '--default-search', 'ytsearch',
            '--no-playlist', '--no-check-certificate', '--geo-bypass'
        ]
    try:
        # Get the output and analyze it
        output = subprocess.check_output(command).decode('utf-8')
        videos = [json.loads(line) for line in output.splitlines()]
        # Simplify the results for displaying to the user
        simplified_results = []
        for video in videos:
            simplified_results.append({
                "title": video.get("title", "N/A"),
                "url": video.get("webpage_url", "N/A"),
                "origin_url": video.get("original_url", "N/A"),
                "duration": str(datetime.timedelta(seconds=video.get("duration", 0))),
                "uploader": video.get("uploader", "N/A")
            })

        return simplified_results

    except subprocess.CalledProcessError:
        return []
print(search("việt nam",10))