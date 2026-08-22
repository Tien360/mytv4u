import urllib.request
import json

req = urllib.request.Request('https://pub.dev/api/packages/file_picker')
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    print(data['latest']['version'])
