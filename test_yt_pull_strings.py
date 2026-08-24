import urllib.request
import re

url = "https://www.youtube.com/results?search_query=Pull+Strings+trailer"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'"videoRenderer":\{"videoId":"([a-zA-Z0-9_-]{11})"', html)
    if match:
        print(f"Regex found YouTube ID: {match.group(1)}")
    else:
        print("Regex not found.")
except Exception as e:
    print(e)
