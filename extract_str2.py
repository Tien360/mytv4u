with open("T:/Project/Phim/mytv4u_flutter/lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(ord(c) > 127 for c in line):
        print(f"{i+1}: {line.strip()}")
