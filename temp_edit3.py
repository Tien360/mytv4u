with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("""              return HoverEpisodeButton(
                text: dispName,
                onTap: () async {""",
"""              return HoverEpisodeButton(
                text: dispName,
                progress: _episodeProgressMap[ep.name] ?? 0.0,
                progressColor: _dominantColor,
                onTap: () async {""")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated HoverEpisodeButton calls")
