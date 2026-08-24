import urllib.request
import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = "https://html.duckduckgo.com/html/?q=site:youtube.com+Pull+Strings+trailer"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', class_='result__url'):
        href = a.get('href')
        if 'youtube.com/watch?v=' in href:
            match = re.search(r'v=([a-zA-Z0-9_-]{11})', href)
            if match:
                print("DDG found ID:", match.group(1))
                break
except Exception as e:
    print(e)
