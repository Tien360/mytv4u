
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()
import re
match = re.search(r'// Share & Trailer Buttons.*?Row\([\s\S]*?children: \[([\s\S]*?)\]\s*\),', content)
if match:
    print('Found buttons!')
else:
    print('Not found')

