import re, sys
sys.stdout.reconfigure(encoding="utf-8")
with open("yt_playables_home.html", "r", encoding="utf-8") as f:
    data = f.read()

print("12+:", len(re.findall(r'12\+', data, re.IGNORECASE)))
print("Stealth Master:", len(re.findall(r'Stealth Master', data, re.IGNORECASE)))
