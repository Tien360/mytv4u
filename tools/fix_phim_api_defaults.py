
with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
'''            'phim4k',
            'free1',''',
'''            'film4knet',
            'phim4k',
            'free1',''')
text = text.replace(
'''              'phim4k',
              'free1',''',
'''              'film4knet',
              'phim4k',
              'free1',''')

with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done')

