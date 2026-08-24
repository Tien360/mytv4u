import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')
tmdb_api_key = "49a1dccb31b34a10e8d357b98a3b8d9e"
year = "2026"

url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={urllib.parse.quote('Pull Strings')}&language=vi&year={year}"
try:
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    if data['results']:
        print("Match title:", data['results'][0]['title'])
        print("Match ID:", data['results'][0]['id'])
    else:
        print("No match for Pull Strings")
except Exception as e:
    pass

url2 = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={urllib.parse.quote('Sư Huynh Quá Cẩn Trọng')}&language=vi&year={year}"
try:
    res = urllib.request.urlopen(url2).read().decode('utf-8')
    data = json.loads(res)
    if data['results']:
        print("Match title2:", data['results'][0]['title'])
        print("Match ID2:", data['results'][0]['id'])
    else:
        print("No match for Sư Huynh Quá Cẩn Trọng")
except Exception as e:
    pass
