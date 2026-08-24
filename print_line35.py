with open("lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "void _showOpenUrlDialog" in line:
        for j in range(max(0, i-2), min(len(lines), i+65)):
            print(f"{j+1}: {lines[j].encode('ascii', 'ignore').decode('ascii').rstrip()}")
        break
