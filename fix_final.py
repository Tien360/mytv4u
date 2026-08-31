def fix_final_name(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target1 = "_episodes[_currentIndex].name = newEps[0].name;"
    replacement1 = '''_episodes[_currentIndex] = Episode(
                 name: newEps[0].name,
                 slug: _episodes[_currentIndex].slug,
                 m3u8Url: _episodes[_currentIndex].m3u8Url,
                 embedUrl: _episodes[_currentIndex].embedUrl,
                 filename: _episodes[_currentIndex].filename,
               );'''
    content = content.replace(target1, replacement1)

    target2 = "_episodes[_currentIndex].name = data['title'];"
    replacement2 = '''_episodes[_currentIndex] = Episode(
              name: data['title'],
              slug: _episodes[_currentIndex].slug,
              m3u8Url: _episodes[_currentIndex].m3u8Url,
              embedUrl: _episodes[_currentIndex].embedUrl,
              filename: _episodes[_currentIndex].filename,
            );'''
    content = content.replace(target2, replacement2)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_final_name('lib/screens/player_screen.dart')
print("Fixed final name assignment")
