
import urllib.request, json
url = 'https://api.themoviedb.org/3/tv/242247/images?api_key=42890db72186981881512db47164ff58'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    print('Logos:', len(data.get('logos', [])))

