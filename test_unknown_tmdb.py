import urllib.request
import json
url = "https://api.themoviedb.org/3/search/multi?api_key=e9e9d8da18ae29fc430845952232787c&query=Unknown+Title&language=en-US"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    res = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    print("Results:", len(data['results']))
    if data['results']:
        print("First id:", data['results'][0]['id'])
except Exception as e:
    print(e)
