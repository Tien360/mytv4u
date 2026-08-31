import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("Webview(_webController)")
if idx != -1:
    print(content[idx-1000:idx+2000])
