
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
'''      'phim4k': true,''',
'''      'phim4k': true,
      'film4knet': true,''')

text = text.replace(
'''      'phim4k': 'Phim 4K',''',
'''      'phim4k': 'Phim 4K',
      'film4knet': 'Film4K.net',''')

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done')

