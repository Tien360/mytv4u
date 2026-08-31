import sys
sys.stdout.reconfigure(encoding='utf-8')
with open("yt_game.json", "r", encoding="utf-8") as f:
    data = f.read()

idx = data.find("Stealth Master")
while idx != -1:
    print("MATCH:", data[idx-100:idx+300])
    print("-" * 50)
    idx = data.find("Stealth Master", idx+1)
