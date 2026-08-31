import sys
with open('lib/widgets/ambient_background.dart', 'r', encoding='utf-8') as f:
    for line in f.readlines()[15:35]:
        print(line, end='')
