import json
import urllib.request
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
api_key = "e9e9d8da18ae29fc430845952232787c"

def fetch_list(url):
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
            results = data.get("results", [])
            return [x.get("name") or x.get("title") for x in results[:15]]
    except Exception as e:
        return [str(e)]

url_movie = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=vi-VN&with_watch_providers=8&watch_region=US&sort_by=popularity.desc"
print("Movies on Netflix US:")
for title in fetch_list(url_movie):
    print("-", title)
