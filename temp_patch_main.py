import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/main.dart', 'r', encoding='utf-8') as f:
    content = f.read()

search = "home: const MainScreen(),"
replace = "home: const SettingsScreen(),"
if search in content:
    content = content.replace(search, replace)
    print("Patched main.dart to load SettingsScreen!")

with open('lib/main.dart', 'w', encoding='utf-8') as f:
    f.write(content)
