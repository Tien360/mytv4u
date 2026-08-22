
import urllib.request, json
url = 'https://phimapi.com/v1/api/tim-kiem?keyword=con'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    print(list(data['data']['items'][0].keys()))

