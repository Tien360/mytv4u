import re

with open("lib/api/premium_api.dart", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('"link": "premium://$rawId",', '"link": "premium://play/$rawId",')
content = content.replace('"link_m3u8": "premium://$rawId",', '"link_m3u8": "premium://play/$rawId",')

with open("lib/api/premium_api.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched premium_api.dart to use premium://play/")
