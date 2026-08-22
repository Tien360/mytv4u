with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'FilePicker.pickFiles' in line:
        for j in range(i, i+15):
            print(lines[j], end='')
        print("-------")
