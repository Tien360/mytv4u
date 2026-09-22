import re
with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

pattern = r"\|\|\s*_currentUrl\.startsWith\('premium://'\)"

text, count = re.subn(pattern, "", text)
print(f"Replaced {count} times")

with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
