import re
with open("T:/Project/Phim/mytv4u_flutter/lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# simple regex to extract strings in single quotes
matches = re.findall(r"'([^'a-zA-Z0-9_\-\.]+[\w\s]+)'", text)
print(set(matches))
