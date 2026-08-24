import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://phim.nguonc.com/api/film/su-huynh-qua-can-trong"
try:
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    print("Name:", data['movie']['name'])
    print("Orig Name:", data['movie']['original_name'])
except Exception as e:
    print(e)
