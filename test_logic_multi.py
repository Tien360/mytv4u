import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')
tmdb_api_key = "e9e9d8da18ae29fc430845952232787c"

url = f"https://api.themoviedb.org/3/search/multi?query={urllib.parse.quote('Pull Strings')}&api_key={tmdb_api_key}&language=vi-VN"
try:
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    print("Multi search found:", len(data['results']))
    for m in data['results']:
        print("Match:", m.get('title', m.get('name')), "Type:", m.get('media_type'))
except Exception as e:
    print(e)
