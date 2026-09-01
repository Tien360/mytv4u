import json
import urllib.request

url = "https://api.themoviedb.org/3/tv/1399?api_key=e9e9d8da18ae29fc430845952232787c&language=en"
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
        print("Last ep:", data.get('last_episode_to_air'))
except Exception as e:
    print(e)
