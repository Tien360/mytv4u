import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://tinhlagi.pro/sport/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    with open('sport_html.txt', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved to sport_html.txt. Length:", len(html))
except Exception as e:
    print("Error:", e)
