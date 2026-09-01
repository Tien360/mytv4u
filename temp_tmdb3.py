import json
import urllib.request

url = "https://api.themoviedb.org/3/tv/1399?api_key=e9e9d8da18ae29fc430845952232787c&language=vi"
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
        print("created_by:", [c['name'] for c in data.get('created_by', [])])
except Exception as e:
    print(e)
