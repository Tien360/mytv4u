
import urllib.request, json
url = 'https://api.themoviedb.org/3/search/tv?api_key=42890db72186981881512db47164ff58&query=Love+Next+Door'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    print(data['results'][0]['id'])

