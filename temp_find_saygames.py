import sys
sys.stdout.reconfigure(encoding='utf-8')
with open("yt_game.json", "r", encoding="utf-8") as f:
    data = f.read()

idx = data.find("SayGames")
if idx != -1:
    print(data[idx-100:idx+200])
else:
    print("Not found")
