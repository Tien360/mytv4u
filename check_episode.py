
with open('lib/models/movie.dart', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.findall(r'class Episode \{[\s\S]*?\}', content)
if matches:
    print(matches[0])

