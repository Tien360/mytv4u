import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

import re
keys = re.findall(r'SizedBox\(key: (_[a-zA-Z]+Key)\)', content)
print("Page keys order:", keys)

sidebar_keys = re.findall(r'_buildSidebarItem\([^,]+,\s*[^,]+,\s*(_[a-zA-Z]+Key)\)', content)
print("Sidebar keys order:", sidebar_keys)
