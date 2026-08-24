with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(20):
    print(lines[i].encode('ascii', 'ignore').decode('ascii').rstrip())
