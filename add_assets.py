content = open('pubspec.yaml', 'r', encoding='utf-8').read()
if '- assets/images/' not in content:
    content = content.replace('  assets:', '  assets:\n    - assets/images/')
    open('pubspec.yaml', 'w', encoding='utf-8').write(content)
