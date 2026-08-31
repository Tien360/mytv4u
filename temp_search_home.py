import re, sys
sys.stdout.reconfigure(encoding="utf-8")
with open("yt_playables_home.html", "r", encoding="utf-8") as f:
    data = f.read()

print("86 Tr:", re.findall(r'.{0,40}86 Tr.{0,40}', data, re.IGNORECASE))
print("IARC:", re.findall(r'.{0,40}IARC.{0,40}', data, re.IGNORECASE))
print("lượt chơi:", re.findall(r'.{0,40}lượt chơi.{0,40}', data, re.IGNORECASE))
