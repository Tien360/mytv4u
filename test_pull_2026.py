import urllib.request
import json

url = "https://www.youtube.com/results?search_query=+Pull+Strings+2026+trailer"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    startIndex = html.find('var ytInitialData = {')
    endIndex = html.find(';</script>', startIndex)
    jsonStr = html[startIndex + 20:endIndex]
    data = json.loads(jsonStr)
    contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
    for section in contents:
        if 'itemSectionRenderer' in section:
            items = section['itemSectionRenderer'].get('contents', [])
            for item in items[:2]:
                if 'videoRenderer' in item:
                    print("ID:", item['videoRenderer']['videoId'])
except Exception as e:
    print(e)
