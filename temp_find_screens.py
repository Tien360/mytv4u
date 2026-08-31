import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/main_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("final List<Widget> _screens")
if idx != -1:
    print(content[idx:idx+800])
