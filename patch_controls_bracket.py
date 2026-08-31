path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
for i in range(len(lines)):
    if 'child: AnimatedOpacity(' in lines[i]:
        open_b = 0
        started = False
        for j in range(i, len(lines)):
            if 'AnimatedOpacity(' in lines[j]:
                started = True
            if started:
                open_b += lines[j].count('(')
                open_b -= lines[j].count(')')
                if open_b == 0:
                    lines.insert(j+1, "                ),\n")
                    break
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Added closing bracket for controls layer")
