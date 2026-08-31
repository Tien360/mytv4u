import re
def fix_title_update(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # In _loadLazyPlaylist
    target = '''_episodes[_currentIndex] = Episode(
                 name: newEps[0].name,
                 slug: _episodes[_currentIndex].slug,
                 m3u8Url: _episodes[_currentIndex].m3u8Url,
                 embedUrl: _episodes[_currentIndex].embedUrl,
                 filename: _episodes[_currentIndex].filename,
               );'''
    replacement = target + '''
               if (_isYoutubeLink || widget.lazyPlaylistUrl != null) {
                 _currentTitle = newEps[0].name;
               }'''
    if "if (_isYoutubeLink || widget.lazyPlaylistUrl != null) {" not in content.split("_loadLazyPlaylist")[1]:
        content = content.replace(target, replacement)
        
    # In _fetchYoutubeQualities
    target2 = '''_episodes[_currentIndex] = Episode(
              name: data['title'],
              slug: _episodes[_currentIndex].slug,
              m3u8Url: _episodes[_currentIndex].m3u8Url,
              embedUrl: _episodes[_currentIndex].embedUrl,
              filename: _episodes[_currentIndex].filename,
            );'''
    replacement2 = target2 + '''
            if (_isYoutubeLink || widget.lazyPlaylistUrl != null) {
              _currentTitle = data['title'];
            }'''
    content = content.replace(target2, replacement2)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_title_update('lib/screens/player_screen.dart')
print("Fixed title updates")
