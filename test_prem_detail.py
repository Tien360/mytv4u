import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://dogtail.oxaliplatin.workers.dev/api/premium/detail/su-huynh-qua-can-trong"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    item = data.get('movie', data.get('item', {}))
    print("Name:", item.get('name'))
    print("Original Name:", item.get('original_name'))
except Exception as e:
    print(e)
