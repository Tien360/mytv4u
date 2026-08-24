import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = "https://dogtail.oxaliplatin.workers.dev/api/premium/phim-bo"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    for p in data['items']:
        if 'sư huynh' in p['name'].lower() or 'pull' in p['original_name'].lower():
            print(f"Name: '{p['name']}' Original: '{p['original_name']}'")
except Exception as e:
    print(e)
