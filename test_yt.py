import urllib.request
import re

url = "https://www.youtube.com/results?search_query=random_obscure_movie_name+trailer"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'/watch\?v=([a-zA-Z0-9_-]{11})', html)
    if match:
        print(f"Found YouTube ID: {match.group(1)}")
        
        # Let's print out the context around it
        idx = html.find(match.group(0))
        print(html[idx-100:idx+100])
except Exception as e:
    print(e)
