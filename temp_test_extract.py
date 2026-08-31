import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open("yt_game.json", "r", encoding="utf-8") as f:
    data = f.read()

# Try to find description
desc_match = re.search(r'"description":\{"simpleText":"(.*?)"\}', data)
if desc_match:
    print("DESC:", desc_match.group(1))

# Try to find publisher
pub_match = re.search(r'"developerName":\{"simpleText":"(.*?)"\}', data)
if pub_match:
    print("PUB:", pub_match.group(1))
