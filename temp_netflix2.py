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
            return [x.get("name") or x.get("title") for x in results[:10]]
    except Exception as e:
        return str(e)

# 1. Netflix Original Series (TV) sorted by popularity
url_tv = f"https://api.themoviedb.org/3/discover/tv?api_key={api_key}&language=vi-VN&with_networks=213&sort_by=popularity.desc"
print("Netflix Original Series (Phim Bộ Gốc Netflix):")
for title in fetch_list(url_tv):
    print("-", title)

# 2. Movies available on Netflix (US or VN) sorted by popularity
url_movie = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=vi-VN&with_watch_providers=8&watch_region=VN&sort_by=popularity.desc"
print("\nMovies on Netflix (Phim Lẻ có trên Netflix VN):")
for title in fetch_list(url_movie):
    print("-", title)

