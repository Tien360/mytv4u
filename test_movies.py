import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = f"https://api.themoviedb.org/3/search/movie?api_key=e9e9d8da18ae29fc430845952232787c&query={urllib.parse.quote('Pull Strings')}&language=en-US"
try:
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    print("Found movies:", len(data['results']))
    for m in data['results']:
        print("Match:", m.get('title'), m.get('id'))
except Exception as e:
    print(e)
