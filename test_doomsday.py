import urllib.request
from bs4 import BeautifulSoup
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
url = "https://www.youtube.com/results?search_query=Avengers+Doomsday+Special+Look+Marvel+Vietnam"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'"videoRenderer":\{"videoId":"([a-zA-Z0-9_-]{11})"', html)
    if match:
        print("Doomsday ID:", match.group(1))
    else:
        print("Not found")
except Exception as e:
    print(e)
