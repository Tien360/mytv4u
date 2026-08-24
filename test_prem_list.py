import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = "https://dogtail.oxaliplatin.workers.dev/api/premium"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    items = data.get('items', [])
    for item in items:
        if 'su-huynh' in item.get('slug', ''):
            print("Found in premium list:", item.get('name'), "Slug:", item.get('slug'))
except Exception as e:
    print(e)
