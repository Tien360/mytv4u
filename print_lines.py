lines = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read().splitlines()
with open('temp_lines.txt', 'w', encoding='utf-8') as f:
    for i in range(750, 800):
        f.write(f"{i+1}: {lines[i]}\n")
