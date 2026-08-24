import urllib.request
import re
import json

url = "https://www.youtube.com/results?search_query=trailer"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
    if match:
        data = json.loads(match.group(1))
        contents = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
        for section in contents:
            if 'itemSectionRenderer' in section:
                for item in section['itemSectionRenderer']['contents']:
                    if 'videoRenderer' in item:
                        print("Found organic ID:", item['videoRenderer']['videoId'])
                        break
                break
except Exception as e:
    print(e)
