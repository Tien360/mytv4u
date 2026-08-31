import urllib.request
import re

url = "https://www.youtube.com/playables/UgkxAa2Gygx3bQRx4kOraVwUFW_3mO1tH0h5"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
    if match:
        data = match.group(1)
        print("Found ytInitialData! Length:", len(data))
        if "Stealth Master" in data: print("Contains title")
        if "SayGames" in data: print("Contains publisher (SayGames)")
        # Just write the data to a file so we can inspect it
        with open("yt_game.json", "w", encoding="utf-8") as f:
            f.write(data)
    else:
        print("No ytInitialData found")
except Exception as e:
    print(e)
