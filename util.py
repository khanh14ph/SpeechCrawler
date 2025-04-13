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
   
