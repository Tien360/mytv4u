with open("lib/screens/movie_detail_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = lines[:846] + lines[941:]

with open("lib/screens/movie_detail_screen.dart", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Deleted bad lines")
