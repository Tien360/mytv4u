import urllib.request
import json
import urllib.parse
import sys

sys.stdout.reconfigure(encoding='utf-8')
tmdb_api_key = "49a1dccb31b34a10e8d357b98a3b8d9e"

url = f"https://api.themoviedb.org/3/search/multi?api_key={tmdb_api_key}&query={urllib.parse.quote('Pull Strings')}&language=vi-VN"
try:
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    if data['results']:
        for result in data['results'][:3]:
            print(result.get('name', result.get('title')))
            print("Year:", result.get('release_date', result.get('first_air_date')))
            print("Type:", result.get('media_type'))
            print("ID:", result['id'])
            print("---")
    else:
        print("No match for Pull Strings")
except Exception as e:
    print(e)

