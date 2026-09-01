import urllib.request

req = urllib.request.Request("https://film4k.net", headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        print("URL:", response.url)
except Exception as e:
    print("Error:", e)
