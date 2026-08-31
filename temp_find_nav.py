import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.finditer(r'Navigator\.push\(', content)
for m in matches:
    idx = m.start()
    print("--------------------")
    print(content[idx-300:idx+200])
