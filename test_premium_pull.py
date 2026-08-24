import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = "https://dogtail.oxaliplatin.workers.dev/api/premium/movies?keyword=pull"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    for p in data['items']:
        print(f"Name: '{p['name']}' Original: '{p['original_name']}'")
except Exception as e:
    print(e)
