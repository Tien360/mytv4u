import json
import urllib.request

url = "https://api.themoviedb.org/3/tv/1399/season/1?api_key=e9e9d8da18ae29fc430845952232787c&language=vi"
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
        ep = data["episodes"][0]
        print("Keys:", ep.keys())
        print("Guest stars count:", len(ep.get("guest_stars", [])))
        if len(ep.get("guest_stars", [])) > 0:
            print("First guest:", ep["guest_stars"][0])
        print("Crew count:", len(ep.get("crew", [])))
        if len(ep.get("crew", [])) > 0:
            print("First crew:", ep["crew"][0])
        print("Vote average:", ep.get("vote_average"))
except Exception as e:
    print(e)
