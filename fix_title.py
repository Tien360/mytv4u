def fix_current_title(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target = "    _currentTitle = '\ - \';"
    replacement = '''    if (_isYoutubeLink || widget.lazyPlaylistUrl != null) {
      _currentTitle = ep.name;
    } else {
      _currentTitle = '\ - \';
    }'''
    content = content.replace(target, replacement)

    # And in _loadLazyPlaylist, we must also update _currentTitle!
    target2 = "_episodes[_currentIndex].name = newEps[0].name;"
    replacement2 = '''_episodes[_currentIndex] = Episode(
              name: newEps[0].name,
              slug: _episodes[_currentIndex].slug,
              m3u8Url: _episodes[_currentIndex].m3u8Url,
              embedUrl: _episodes[_currentIndex].embedUrl,
              filename: _episodes[_currentIndex].filename,
            );
            if (_isYoutubeLink || widget.lazyPlaylistUrl != null) {
              _currentTitle = newEps[0].name;
            }'''
    # we already replaced target2 in previous patch, let's search for what we placed
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_current_title('lib/screens/player_screen.dart')
print("Fixed current title init")
