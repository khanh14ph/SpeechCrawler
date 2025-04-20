import requests
from bs4 import BeautifulSoup

# YouTube Video ID
def get_title(video_id):

# YouTube Video URL
    url = f'https://www.youtube.com/watch?v={video_id}'

    # Extracting HTML Code of the Video Page:
    response = requests.get(url)
    html_content = response.text

    # Processing the HTML Code with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting <title> tag's content
    title_tag = soup.find('meta', property='og:title')
    video_title = title_tag['content'] if title_tag else 'Title not found'

    return video_title
   
if __name__ == "__main__":
    import json
    import glob
    from tqdm import tqdm
    lst=glob.glob("/Users/khanh/dev/crawler/database/downloaded_subtitle/*")
    for i in tqdm(lst):
        print(i)
        metadata=json.load(open(i))
        if metadata["language"] == "de":
            if "title" not in metadata:
                metadata["title"] = get_title(metadata["id"])
            for j in metadata["subtitles"]:
                j["text"] = j["text"].replace("'","").replace("\"","").replace("’","").replace("“","").replace("”","").replace("‘","")
            with open(i, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4,ensure_ascii=False)


