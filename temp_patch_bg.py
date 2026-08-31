import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

bg_search = "      backgroundColor: const Color(0xFF000000),"
bg_replace = "      backgroundColor: Colors.transparent,"
if bg_search in content:
    content = content.replace(bg_search, bg_replace)
    print("Replaced background color!")
else:
    print("Background color not found!")
    
with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
