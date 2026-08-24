import urllib.request

url = "https://tinhlagi.pro/sport/livescore_data.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    data = urllib.request.urlopen(req).read().decode('utf-8')
    with open('livescore.json', 'w', encoding='utf-8') as f:
        f.write(data)
    print("Saved livescore.json, length:", len(data))
    print(data[:500])
except Exception as e:
    print("Error:", e)
