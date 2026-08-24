with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extract block 908-995
block = lines[907:995]
lines = lines[:907] + lines[995:]

# Modify block for better spacing
for i in range(len(block)):
    block[i] = block[i].replace("const SizedBox(height: 8)", "const SizedBox(height: 16)")

# Find insertion point
insert_idx = -1
for i, line in enumerate(lines):
    if "const SizedBox(width: 40)," in line:
        insert_idx = i - 3  # Insert before `],`
        break

if insert_idx != -1:
    lines = lines[:insert_idx] + ["\n                                          const SizedBox(height: 16),\n"] + block + lines[insert_idx:]
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Fixed!")
else:
    print("Not found insert_idx")
