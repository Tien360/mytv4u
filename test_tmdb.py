import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Mock what PhimApi._searchTmdb does
tmdb_api_key = "49a1dccb31b34a10e8d357b98a3b8d9e"
title = "Sư Huynh Quá Cẩn Trọng"
original_title = "Pull Strings"
year = "2024" # Oh wait, in the screenshot the year is 2026!

url1 = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={urllib.parse.quote(original_title)}&language=vi"
try:
    res = urllib.request.urlopen(url1).read().decode('utf-8')
    data = json.loads(res)
    if data['results']:
        print("Match original_title:", data['results'][0]['title'])
except Exception as e:
    pass

url2 = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={urllib.parse.quote(title)}&language=vi"
try:
    res = urllib.request.urlopen(url2).read().decode('utf-8')
    data = json.loads(res)
    if data['results']:
        print("Match title:", data['results'][0]['title'])
except Exception as e:
    pass

