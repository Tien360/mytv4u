import sys

with open('tools/release.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("['build', 'windows', '--no-pub']", "['build', 'windows', '--verbose', '--no-pub']")

with open('tools/release.dart', 'w', encoding='utf-8') as f:
    f.write(text)
