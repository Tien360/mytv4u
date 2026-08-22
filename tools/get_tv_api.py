
import urllib.request
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    c = urllib.request.urlopen(urllib.request.Request('https://film4k.net/api/tv/channels', headers=headers)).read()
    with open('tools/channels.json', 'wb') as f: f.write(c)
    print('channels.json downloaded')
    e = urllib.request.urlopen(urllib.request.Request('https://film4k.net/api/tv/events', headers=headers)).read()
    with open('tools/events.json', 'wb') as f: f.write(e)
    print('events.json downloaded')
except Exception as e:
    print('Error:', e)

