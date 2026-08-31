import sys

with open('lib/screens/main_screen.dart', 'r', encoding='utf-8') as f:
    c = f.read()

target = "const GamingScreen(key: PageStorageKey('GamingScreen')),"
new_target = "GamingScreen(key: _gamingKey),"
if target in c:
    c = c.replace(target, new_target)
    print("Fixed GamingScreen key")
else:
    print("Could not find GamingScreen key")

with open('lib/screens/main_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c)

