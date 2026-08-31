import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("_isUsingWebview =")
if idx != -1:
    print(content[idx-100:idx+400])
