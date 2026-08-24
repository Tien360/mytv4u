import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = "https://www.youtube.com/results?search_query=Pull+Strings+trailer"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
    if match:
        data = json.loads(match.group(1))
        # trace structure
        print("keys:", data.keys())
        p_contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
        print("section contents len:", len(p_contents))
        if p_contents:
            for s in p_contents:
                print(" section key:", list(s.keys())[0] if s else "none")
                if 'itemSectionRenderer' in s:
                    items = s['itemSectionRenderer'].get('contents', [])
                    print("  items len:", len(items))
                    for i in items:
                        if 'videoRenderer' in i:
                            print("   found video:", i['videoRenderer']['videoId'])
                            break
                    break
except Exception as e:
    print(e)
