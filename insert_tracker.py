import re

with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

target = r"(_buildRichText\('Doanh thu: ', '.*?'\),\s*\]\,\s*)"

match = re.search(target, text, flags=re.DOTALL)
if match:
    replacement = match.group(1) + "NextEpisodeTracker(movie: _movie, tmdbDetails: _tmdbDetails, phraseSeed: _phraseSeed),\n"
    text = text.replace(match.group(1), replacement)
    print("Injected NextEpisodeTracker call")
else:
    print("Could not find budget/revenue target block!")

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
