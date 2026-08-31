with open("T:/Project/Phim/mytv4u_flutter/lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("vietnamese_lines.txt", "w", encoding="utf-8") as out:
    for i, line in enumerate(lines):
        if any(ord(c) > 127 for c in line) and "L10n.t" not in line:
            out.write(f"{i+1}: {line.strip()}\n")
