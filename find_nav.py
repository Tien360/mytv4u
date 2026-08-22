
with open('lib/screens/home_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()
import re
# Print all NavigationRailDestination or BottomNavigationBarItem to see the current tabs
matches = re.findall(r'NavigationRailDestination\([^)]+\)', content)
if not matches:
    matches = re.findall(r'BottomNavigationBarItem\([^)]+\)', content)
for m in matches:
    print(m)

