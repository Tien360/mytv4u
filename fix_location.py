with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

block = lines[1805:1893]
lines = lines[:1805] + lines[1893:]

# Now we need to find where to insert it.
# The `],` that closes `if (_directorsTmdb.isNotEmpty) ...[` was at 1899 before removal.
# Let's search for `}).toList(),` which is now at 1897 - 88 = 1809
insert_idx = -1
for i, line in enumerate(lines):
    if "}).toList()," in line and "]," in lines[i+1]:
        insert_idx = i + 2
        break

if insert_idx != -1:
    lines = lines[:insert_idx] + block + lines[insert_idx:]
    with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Fixed!")
else:
    print("Not found insert_idx")
