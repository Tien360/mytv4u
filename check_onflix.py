
import urllib.request
req = urllib.request.Request('https://onflix.lat/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        with open('onflix.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print('Fetched HTML')
except Exception as e:
    print(e)

