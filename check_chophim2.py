
import urllib.request, re
req = urllib.request.Request('https://chophim.app/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        match = re.search(r'(.{0,150}Sticky Love.{0,150})', html)
        if match:
            # Save to file to avoid encoding issues on print
            with open('sticky.txt', 'w', encoding='utf-8') as f:
                f.write(match.group(1))
        else:
            print('Not found')
except Exception as e:
    print(e)

