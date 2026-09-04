import sys

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

c = re.sub(
    r'SingleChildScrollView\(\s*scrollDirection:\s*Axis\.horizontal,\s*child:\s*Row\(\s*children:\s*List\.generate\(maxChunks,\s*\(chunkIdx\)\s*\{',
    r'Wrap(\n                spacing: 8.0,\n                runSpacing: 8.0,\n                children: List.generate(maxChunks, (chunkIdx) {',
    c
)

c = re.sub(
    r'(\s*child:\s*Text\([\s\S]*?\),\s*\),\s*\),\s*\),\s*\);)\s*\}\),\s*\),\s*\),',
    r'\1\n                  }),\n              ),',
    c
)

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed Wrap in MovieDetailScreen")
