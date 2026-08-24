import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Find the actors section
idx = content.find("L10n.t('actors')")
if idx != -1:
    print(content[idx:idx+3500])
else:
    print("Not found")
