import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
tmdb_api_key = "e9e9d8da18ae29fc430845952232787c"

url = f"https://api.themoviedb.org/3/tv/272938/videos?api_key={tmdb_api_key}"
try:
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    print("Videos found:", len(data['results']))
    for v in data['results']:
        print("Video Key:", v['key'], "Site:", v['site'], "Type:", v['type'])
except Exception as e:
    print(e)
