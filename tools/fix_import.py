
import re

with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

if 'film4knet_api.dart' not in text:
    text = text.replace('import ''package:http/http.dart'' as http;', 'import ''package:http/http.dart'' as http;\nimport ''film4knet_api.dart'';')
    with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added import')
else:
    print('Import already exists')

