import sys

with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

c = re.sub(
    r'Row\(\s*mainAxisSize: MainAxisSize\.min,\s*children: \[([\s\S]*?)Text\(\s*widget\.episode\.name,',
    r'Row(\n                  children: [\1Expanded(\n                    child: Text(\n                      widget.episode.name,',
    c
)

c = re.sub(
    r'overflow: TextOverflow\.ellipsis,\s*\),\s*\],\s*\),',
    r'overflow: TextOverflow.ellipsis,\n                    ),\n                  ),\n                  ],\n                ),',
    c
)

with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed Expanded in PlayerEpisodeButton")
