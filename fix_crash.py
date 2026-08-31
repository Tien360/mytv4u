import re

def fix_player_crash(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Prevent _initEpisode from playing dummy episodes
    old_init = r"final ep = _episodes\[index\];\s*String targetUrl = ep\.m3u8Url\.isNotEmpty \? ep\.m3u8Url : ep\.embedUrl;"
    new_init = '''final ep = _episodes[index];
    if (ep.name.contains('Đang tải') || ep.name.contains('loading')) {
      return; // Do not pass dummy playlist URLs to media_kit
    }
    String targetUrl = ep.m3u8Url.isNotEmpty ? ep.m3u8Url : ep.embedUrl;'''
    
    content = re.sub(old_init, new_init, content)
    
    # 2. Make _loadLazyPlaylist trigger playback once done
    old_lazy = r"if \(_currentIndex < _episodes\.length && _episodes\[_currentIndex\]\.name\.contains\('loading'\)\) \{\s*_episodes\[_currentIndex\] = Episode\([\s\S]*?if \(_isYoutubeLink \|\| widget\.lazyPlaylistUrl != null\) \{\s*_currentTitle = newEps\[0\]\.name;\s*\}\s*\}"
    
    new_lazy = '''if (_currentIndex < _episodes.length) {
                // Actually start playing the first fetched video
                _initEpisode(_currentIndex);
             }'''
             
    content = re.sub(old_lazy, new_lazy, content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_player_crash('lib/screens/player_screen.dart')
print("Patched player_screen.dart to prevent playlist crash")
