path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# delete lines 1246 to 1275 inclusive
del lines[1246:1275]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Deleted floating lines")
