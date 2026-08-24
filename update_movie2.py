with open("lib/models/movie.dart", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("required this.totalEpisodes,", "this.totalEpisodes = '',")

with open("lib/models/movie.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated movie.dart totalEpisodes default value")
