import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
tmdb_api_key = "e9e9d8da18ae29fc430845952232787c"

url = f"https://api.themoviedb.org/3/tv/272938/images?api_key={tmdb_api_key}"
try:
    res = urllib.request.urlopen(url).read().decode('utf-8')
    data = json.loads(res)
    for logo in data.get('logos', []):
        print("Logo Lang:", logo.get('iso_639_1'), "File:", logo.get('file_path'))
except Exception as e:
    print(e)
