
import urllib.request
req = urllib.request.Request('https://chophim.app/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        if 'Sticky Love' in html:
            print('Found Sticky Love')
        else:
            print('Not found')
except Exception as e:
    print(e)

