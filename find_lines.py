
with open('lib/screens/library_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'FilePickerResult' in line:
        start = i - 2
        for j in range(start, start+45):
            print(f'{j+1}: {lines[j]}', end='')
        break

