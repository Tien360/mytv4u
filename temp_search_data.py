import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
with open("yt_game.json", "r", encoding="utf-8") as f:
    data = f.read()

# Let's find infoRow
idx = data.find('infoRow')
if idx != -1:
    print(data[max(0, idx-100):min(len(data), idx+500)])
else:
    print("infoRow not found")
