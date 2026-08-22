
import urllib.request, urllib.parse, json
keyword = urllib.parse.quote('Love Next Door')
url = f'https://phimapi.com/v1/api/tim-kiem?keyword={keyword}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    with open('ophim_output.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

