import sys
import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = re.sub(
    r"return HoverEpisodeButton\(\s*text: stream\.name,\s*progress: _episodeProgressMap\['\$\\{_selectedP2pEpisode!\.slug\\} - \$\\{stream\.name\\}'\] \?\? 0\.0,\s*progressColor: _dominantColor,",
    r"return HoverEpisodeButton(\n                  text: stream.name,\n                  progress: _episodeProgressMap['${_selectedP2pEpisode!.slug} - ${stream.name}'] ?? 0.0,\n                  episodeKey: 'continue_${_movie!.name}_${_selectedP2pEpisode!.slug} - ${stream.name}',\n                  durationKey: 'continue_duration_${_movie!.name}_${_selectedP2pEpisode!.slug} - ${stream.name}',\n                  progressColor: _dominantColor,",
    c
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed second HoverEpisodeButton")
