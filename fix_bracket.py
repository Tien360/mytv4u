with open("lib/screens/home_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if "}," in lines[i] and ")," in lines[i+1] and ")," in lines[i+2] and "const SizedBox(height: 16)," in lines[i+3]:
        # found it!
        lines.pop(i+2)
        break

with open("lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.writelines(lines)
