with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace(r"\'${_selectedP2pEpisode!.slug} - ${stream.name}\'", "'${_selectedP2pEpisode!.slug} - ${stream.name}'")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed syntax error")
