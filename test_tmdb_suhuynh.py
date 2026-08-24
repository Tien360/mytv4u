import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')
tmdb_api_key = "e9e9d8da18ae29fc430845952232787c"
year = "2026"

url = f"https://api.themoviedb.org/3/search/multi?api_key={tmdb_api_key}&query={urllib.parse.quote('Sư Huynh Quá Cẩn Trọng')}&language=vi-VN"
try:
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    found = False
    for m in data['results']:
        y = m.get('release_date', m.get('first_air_date', ''))
        if y.startswith(year):
            print("Match:", m.get('title', m.get('name')))
            found = True
    if not found:
        print("No match for Sư Huynh Quá Cẩn Trọng with year 2026")
except Exception as e:
    print(e)
