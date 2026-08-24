import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')
tmdb_api_key = "e9e9d8da18ae29fc430845952232787c"

url = f"https://api.themoviedb.org/3/search/multi?api_key={tmdb_api_key}&query={urllib.parse.quote('Pull Strings')}&language=vi-VN"
try:
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    print("Found:", len(data['results']))
    for m in data['results']:
        y = m.get('release_date', m.get('first_air_date', ''))
        print(m.get('title', m.get('name')), y)
except Exception as e:
    print(e)
