import urllib.request
import re

html_url = 'https://film4k.net/tv'
req = urllib.request.Request(html_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    js_path = re.search(r'src="(/assets/index-[^\"]+\.js)"', html)
    if js_path:
        js_url = 'https://film4k.net' + js_path.group(1)
        js_content = urllib.request.urlopen(urllib.request.Request(js_url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
        
        # Look for API endpoints or m3u8 links or JSON data in JS
        urls = re.findall(r'https?://[^\s"\'\]+', js_content)
        print('Found URLs in main JS:')
        for u in set(urls):
            if '.json' in u or '.m3u8' in u or '.txt' in u or 'api' in u or 'github' in u:
                print(u)
    else:
        print('Could not find JS path')
except Exception as e:
    print('Error:', e)
