import re

with open("lib/screens/yt_player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r"OpenSubtitlesApi\.fetchSubtitles\(.*?\);", "// OpenSubtitlesApi.fetchSubtitles();", content, flags=re.DOTALL)

with open("lib/screens/yt_player_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
