import re
import codecs

with open('lib/api/tv_api.dart', 'r', encoding='utf-8') as f:
    dart_code = f.read()

channel_blocks = re.findall(r'(TvChannel\([^)]+\))', dart_code, re.DOTALL)
our_channels = []
for block in channel_blocks:
    id_match = re.search(r"id:\s*'([^']+)'", block)
    name_match = re.search(r"name:\s*'([^']+)'", block)
    if id_match and name_match: 
        our_channels.append({
            'id': id_match.group(1),
            'name': name_match.group(1)
        })

with codecs.open('our_channels.txt', 'w', encoding='utf-8') as f:
    for i, c in enumerate(our_channels):
        f.write(f"{i+1}. [{c['id']}] {c['name']}\n")
