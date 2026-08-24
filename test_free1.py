import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = "https://phimapi.com/phim/su-huynh-qua-can-trong"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    item = data.get('movie', {})
    print("Name:", item.get('name'))
except Exception as e:
    print(e)
