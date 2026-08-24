import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = f"https://dogtail.oxaliplatin.workers.dev/api/premium/search?keyword={urllib.parse.quote('pull strings')}"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    items = data.get('data', {}).get('items', [])
    for item in items:
        print("Search Result Name:", item.get('name'))
except Exception as e:
    print(e)
