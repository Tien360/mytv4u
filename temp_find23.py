import sys
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(1660, 1690):
    if i < len(lines):
        sys.stdout.buffer.write(f"{i+1}: {lines[i].rstrip()}\n".encode('utf-8'))
