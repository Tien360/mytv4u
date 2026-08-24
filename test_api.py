import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://phim.nguonc.com/api/films/phim-moi-cap-nhat?page=1"
try:
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    for m in data['items']:
        if "sư huynh" in m['name'].lower() or "pull string" in m['original_name'].lower():
            print("Found:", m['name'], "Orig:", m['original_name'])
except Exception as e:
    print(e)
