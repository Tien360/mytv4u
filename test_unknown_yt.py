import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = "https://www.youtube.com/results?search_query=Unknown+Title+trailer"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
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
                    for item in items:
                        if 'videoRenderer' in item:
                            print("Organic ID:", item['videoRenderer']['videoId'])
                            break
                    break
except Exception as e:
    print(e)
