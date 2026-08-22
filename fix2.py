with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "'https://api.themoviedb.org/3/${match['type']}/${match['id']}/images?api_key=$_tmdbApiKey'",
    "\"https://api.themoviedb.org/3/${match['type']}/${match['id']}/images?api_key=$_tmdbApiKey\""
)
content = content.replace(
    "'https://api.themoviedb.org/3/${match['type']}/${match['id']}/credits?api_key=$_tmdbApiKey&language=vi-VN'",
    "\"https://api.themoviedb.org/3/${match['type']}/${match['id']}/credits?api_key=$_tmdbApiKey&language=vi-VN\""
)
content = content.replace(
    "'https://api.themoviedb.org/3/${match['type']}/${match['id']}/videos?api_key=$_tmdbApiKey'",
    "\"https://api.themoviedb.org/3/${match['type']}/${match['id']}/videos?api_key=$_tmdbApiKey\""
)

with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced quotes!")
