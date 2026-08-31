import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if "_isUsingWebview =" in line:
        print("\n".join(lines[i-2:i+10]))
