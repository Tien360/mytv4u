
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '_buildBadgeIcon' in line or '_buildBadge' in line:
        print(f'{i+1}: {line.strip()}')

