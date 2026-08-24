import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = "https://www.youtube.com/results?search_query=Pull+Strings+trailer"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    startIndex = html.find('var ytInitialData = {')
    if startIndex != -1:
        endIndex = html.find(';</script>', startIndex)
        if endIndex != -1:
            jsonStr = html[startIndex + 20:endIndex]
            data = json.loads(jsonStr)
            contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
            for section in contents:
                if 'itemSectionRenderer' in section:
                    items = section['itemSectionRenderer'].get('contents', [])
                    for i, item in enumerate(items[:5]):
                        if 'videoRenderer' in item:
                            print(f"Result {i}:", item['videoRenderer']['videoId'])
except Exception as e:
    print(e)
