with open('lib/screens/main_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

import re
match = re.search(r'IconButton\(\s*icon: const Icon\(Icons\.clear.*?\}\s*,?\s*\)', content, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("Not found")
