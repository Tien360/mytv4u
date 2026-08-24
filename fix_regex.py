with open("lib/screens/sport_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("RegExp(r'(?i) vs ')", "RegExp(r' vs ', caseSensitive: false)")

with open("lib/screens/sport_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Fixed RegExp bug!")
