
import urllib.request
import json
url = 'https://film4k.net/api/home'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    content = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(content)
    with open('tools/film4k_home.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print('Keys:', data.keys())
    for key in data.keys():
        if isinstance(data[key], list):
            print(f'{key}: {len(data[key])} items')
except Exception as e:
    print('Failed:', e)

