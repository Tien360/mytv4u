import urllib.request
req = urllib.request.Request("https://film4k.net", headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as r:
        pass
except Exception as e:
    print(e.read().decode('utf-8')[:500])
