import sys
import json
import urllib.request
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
url = "https://tinhlagi.pro/sport/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    matches = soup.find_all(class_='match-btn')
    for btn in matches[:5]:
        title = btn.get('data-title', '')
        sourcesStr = btn.get('data-sources', '[]')
        sourcesStr = sourcesStr.replace('&quot;', '"')
        try:
            sources = json.loads(sourcesStr)
            print(f"Match: {title}")
            for s in sources:
                print(f"  Link: {s.get('link')}")
        except Exception as e:
            print("Error parsing JSON:", e)
except Exception as e:
    print("Error:", e)
