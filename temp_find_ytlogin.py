import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("Future<void> _openYoutubeLogin()")
if idx != -1:
    print(content[idx:idx+3500])
