import re

with open('lib/api/phim_api.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('''                    Episode(
                      name: 'Full',
                      slug: 'full',
                      m3u8Url: '',
                      embedUrl: 'https://vaplayer.ru/embed/movie/',
                    )
                  ],
                );''', '''                    Episode(
                      name: 'Full',
                      slug: 'full',
                      m3u8Url: '',
                      embedUrl: 'https://vaplayer.ru/embed/movie/',
                    )
                  ],
                ) : null;''')

with open('lib/api/phim_api.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed syntax error')
