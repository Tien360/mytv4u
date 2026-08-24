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
    for m in data['results']:
        y = m.get('release_date', m.get('first_air_date', ''))
        if y.startswith('2026'):
            print("Match:", m.get('title', m.get('name')), m['id'])
except Exception as e:
    print(e)
