import re

with open("pubspec.yaml", "r", encoding="utf-8") as f:
    text = f.read()

# Check if packages are already there to avoid duplicates
if "confetti:" not in text:
    text = text.replace("cupertino_icons:", "confetti: ^0.7.0\n  flutter_animate: ^4.5.0\n  lottie: ^3.1.2\n  cupertino_icons:")

with open("pubspec.yaml", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated pubspec.yaml")
