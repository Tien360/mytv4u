import re
import codecs

with open('lib/api/tv_api.dart', 'r', encoding='utf-8') as f:
    dart_code = f.read()

ids = re.findall(r"id:\s*'([^']+)'", dart_code)
names = re.findall(r"name:\s*'([^']+)'", dart_code)

our_channels = []
for i in range(min(len(ids), len(names))):
    our_channels.append({'id': ids[i], 'name': names[i]})

with codecs.open('our_channels_full.txt', 'w', encoding='utf-8') as f:
    for i, c in enumerate(our_channels):
        f.write(f"{i+1}. [{c['id']}] {c['name']}\n")
