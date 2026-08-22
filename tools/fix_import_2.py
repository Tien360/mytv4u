
import re

with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

if 'import \'film4knet_api.dart\';' not in text:
    text = text.replace('import \'motchill_scraper.dart\';', 'import \'motchill_scraper.dart\';\nimport \'film4knet_api.dart\';')
    with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added import')
else:
    print('Import already exists')

