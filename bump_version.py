import re

content = open('lib/api/update_api.dart', 'r', encoding='utf-8').read()
content = content.replace("static const String currentAppVersion = '26.08.31.19.dev';", "static const String currentAppVersion = '26.08.31.20.dev';")
open('lib/api/update_api.dart', 'w', encoding='utf-8').write(content)
