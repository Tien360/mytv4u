import sys
with open('lib/screens/main_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

import re
c = re.sub(r'IndexedStack\(\s*index:\s*_selectedIndex,\s*children:\s*_screens,\s*\)',
           r'FadeIndexedStack(index: _selectedIndex, children: _screens, duration: const Duration(milliseconds: 300),)', c)

with open('lib/screens/main_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)
print("Regex replace done")
