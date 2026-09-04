with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    c = f.readlines()
for i, l in enumerate(c):
    if "Widget _buildAppInfoCard" in l:
        for x in range(i+45, min(i+110, len(c))):
            print(c[x].encode("ascii", "ignore").decode("ascii"), end="")
        break
