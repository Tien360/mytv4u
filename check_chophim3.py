
import urllib.request, re
req = urllib.request.Request('https://chophim.app/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        match = re.search(r'(.{0,400}Our Sticky Love.{0,100})', html)
        if match:
            with open('sticky.txt', 'w', encoding='utf-8') as f:
                f.write(match.group(1))
except Exception as e:
    print(e)

