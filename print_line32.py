with open("lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "void _showOpenLinkDialog(" in line or "Mở Link" in line:
        for j in range(max(0, i-5), min(len(lines), i+40)):
            print(f"{j+1}: {lines[j].encode('ascii', 'ignore').decode('ascii').rstrip()}")
        break
