
import urllib.request
import re
html_url = 'https://film4k.net/tv'
req = urllib.request.Request(html_url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
match = re.search(r'(/assets/index-.*?\.js)', html)
if match:
    js_url = 'https://film4k.net' + match.group(1)
    print('Downloading:', js_url)
    js_content = urllib.request.urlopen(urllib.request.Request(js_url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
    with open('tools/film4k_index.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    print('Saved to tools/film4k_index.js')

