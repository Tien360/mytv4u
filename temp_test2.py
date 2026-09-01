import urllib.request

req = urllib.request.Request("https://phim4k.net/api", headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=5) as r:
        print("Status:", r.status)
        print("Content:", r.read().decode('utf-8')[:100])
except Exception as e:
    print("Error:", e)
