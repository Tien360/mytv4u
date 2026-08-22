
import urllib.request
import json
url = 'https://film4k.net/api/home?page=2'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    content = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(content)
    print('Page 2 list items:', len(data.get('list', [])))
    if len(data.get('list', [])) > 0:
        print('First item title:', data['list'][0]['title']['vi'])
except Exception as e:
    print('Failed:', e)

