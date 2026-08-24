with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

block = lines[1805:1893]
lines = lines[:1805] + lines[1893:]

# Now `lines` is modified.
# We need to find the `],` that matches the directors block.
# Let's look for `}).toList(),`
insert_idx = -1
for i, line in enumerate(lines):
    if "}).toList()," in line:
        # Check if the next line is `),` or `],`
        for j in range(i+1, i+5):
            if "]," in lines[j]:
                insert_idx = j + 1
                break
        if insert_idx != -1:
            break

if insert_idx != -1:
    lines = lines[:insert_idx] + block + lines[insert_idx:]
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Fixed!")
else:
    print("Not found insert_idx")
