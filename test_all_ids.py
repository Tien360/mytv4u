import urllib.request
import re

url = "https://www.youtube.com/results?search_query=Pull+Strings+trailer"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    matches = re.findall(r'"videoRenderer":\{"videoId":"([a-zA-Z0-9_-]{11})"', html)
    print("Found IDs:", matches[:5])
except Exception as e:
    print(e)
