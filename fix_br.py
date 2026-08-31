path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
# Fix line 2459 back to BorderRadius.circular(20)
for i in range(len(lines)):
    if "borderRadius: 20.0," in lines[i]:
        # check if it's inside BoxDecoration by checking previous lines
        for j in range(i-2, i+1):
            if "BoxDecoration" in lines[j]:
                lines[i] = lines[i].replace("20.0", "BorderRadius.circular(20)")
                break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Fixed borderRadius in BoxDecoration")
