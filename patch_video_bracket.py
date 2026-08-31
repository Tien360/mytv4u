path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
# Find 'child: RepaintBoundary('
for i in range(len(lines)):
    if 'child: RepaintBoundary(' in lines[i]:
        # find the end of Video by counting brackets starting from 'Video('
        open_b = 0
        video_started = False
        for j in range(i+1, len(lines)):
            if 'Video(' in lines[j]:
                video_started = True
            if video_started:
                open_b += lines[j].count('(')
                open_b -= lines[j].count(')')
                if open_b == 0:
                    # we found the end of Video()
                    # add closing bracket for RepaintBoundary on the next line
                    lines.insert(j+1, "                      ),\n")
                    break
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Added closing bracket")
