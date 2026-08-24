import urllib.request
import re

url = "https://www.youtube.com/results?search_query=hello+world"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
    if match:
        print(f"Found YouTube ID: {match.group(1)}")
except Exception as e:
    print(e)
