with open("lib/screens/sport_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(".withOpacity(", ".withValues(alpha: ")

with open("lib/screens/sport_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
