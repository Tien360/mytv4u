import urllib.request
import json
import urllib.parse
import sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://film4k.net/api/title/minions-monsters'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(list(data.keys()))
        print("playable:", data.get('playable'))
except Exception as e:
    print(e)
