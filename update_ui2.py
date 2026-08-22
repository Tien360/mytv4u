
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('backgroundColor: const Color(\n                                                  0xFFF59E0B,\n                                                ),', 'backgroundColor: Colors.white,')
content = content.replace('backgroundColor: const Color(\r\n                                                  0xFFF59E0B,\r\n                                                ),', 'backgroundColor: Colors.white,')
# Let's use regex to be safe
import re
content = re.sub(r'backgroundColor:\s*const\s*Color\(\s*0xFFF59E0B,\s*\),', 'backgroundColor: Colors.white,', content)

with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated share button color')

