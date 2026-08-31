import re

def fix_lazy(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_code = r"if \(_currentIndex < _episodes\.length\) \{\s*// Actually start playing the first fetched video\s*_initEpisode\(_currentIndex\);\s*\}"
    new_code = "if (_currentIndex < _episodes.length) { _currentTitle = _episodes[_currentIndex].name; }"
               
    content = re.sub(old_code, new_code, content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Fixed _loadLazyPlaylist restarting video!")

fix_lazy('lib/screens/player_screen.dart')
