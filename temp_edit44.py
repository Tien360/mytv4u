import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace(
    "await Navigator.push(",
    "await Navigator.push("
) # Wait, how to replace properly?

import re

c = re.sub(
    r'await Navigator\.push\(\s*context,\s*MaterialPageRoute\(\s*builder: \(_\) => PlayerScreen\([\s\S]*?\),\s*\),\s*\);\s*_loadEpisodeProgressAndColor\(\);',
    lambda m: m.group(0) + '\n                    if (mounted) setState(() {});',
    c
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Added setState to rebuild parent after PlayerScreen returns")
