import urllib.request, json
api_key = "e9e9d8da18ae29fc430845952232787c"
imdb_id = "tt0944947" # Game of Thrones

# 1. Find
find_url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&external_source=imdb_id"
req = urllib.request.Request(find_url)
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read())
    tv_results = data.get("tv_results", [])
    if tv_results:
        tmdb_id = tv_results[0]["id"]
        print(f"TMDB ID: {tmdb_id}")

        # 2. Season 1
        season_url = f"https://api.themoviedb.org/3/tv/{tmdb_id}/season/1?api_key={api_key}&language=vi-VN"
        req = urllib.request.Request(season_url)
        with urllib.request.urlopen(req) as res:
            s_data = json.loads(res.read())
            episodes = s_data.get("episodes", [])
            if episodes:
                ep = episodes[0]
                print(f"Ep 1: {ep['name']} | Air: {ep.get('air_date')} | Img: {ep.get('still_path')}")
                print(f"Overview: {ep.get('overview')[:100]}...")
