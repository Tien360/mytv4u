import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = f"https://api.themoviedb.org/3/search/multi?api_key=e9e9d8da18ae29fc430845952232787c&query={urllib.parse.quote('Pull Strings')}&language=en-US"
try:
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    print("Name:", data['results'][0].get('name', data['results'][0].get('title')))
    print("Original:", data['results'][0].get('original_name', data['results'][0].get('original_title')))
except Exception as e:
    print(e)
