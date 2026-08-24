import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = "https://dogtail.oxaliplatin.workers.dev/api/premium/detail/premium-tv-272938"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read().decode('utf-8')
    print(res)
except Exception as e:
    print(e)
