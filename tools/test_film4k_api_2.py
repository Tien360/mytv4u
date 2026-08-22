
import urllib.request
import urllib.parse
import json

url = 'https://film4k.net/api/home?q=' + urllib.parse.quote('one piece')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    content = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(content)
    with open('tools/film4k_search_series.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print('Success')
except Exception as e:
    print('Failed:', e)

