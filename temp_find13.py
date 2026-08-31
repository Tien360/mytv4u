with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(1650, 1690):
    if i < len(lines):
        print(f"{i+1}: {lines[i].rstrip()}")
