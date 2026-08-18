import sys

with open('lib/screens/home_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("'\\ !',", "(L10n.t('hello') ?? 'Xin chào') + ' !',")

with open('lib/screens/home_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
