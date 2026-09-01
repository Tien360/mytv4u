import json
import urllib.request
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
url = "https://api.themoviedb.org/3/certification/movie/list?api_key=e9e9d8da18ae29fc430845952232787c"
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
        certs = data.get("certifications", {})
        print("VN Certs:", certs.get("VN"))
        print("US Certs:", certs.get("US"))
except Exception as e:
    print(e)
