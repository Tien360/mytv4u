
import urllib.request
import urllib.parse
import json

url = 'https://film4k.net/api/title/nguoi-nhen-2002'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    content = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(content)
    with open('tools/film4k_title_movie.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print('Keys:', data.keys())
    print('Has movie.sources?', 'sources' in data['movie'])
except Exception as e:
    print('Failed:', e)

