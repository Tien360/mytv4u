import re

def fix_pop(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target = """// Go back to previous screen automatically when player is closed
          if (mounted) {
            Navigator.pop(context);
          }"""
          
    # Let's search with regex to ignore whitespace differences
    old_code = r"// Go back to previous screen automatically when player is closed\s*if \(mounted\) \{\s*Navigator\.pop\(context\);\s*\}"
            
    new_code = """// Go back to previous screen automatically when player is closed
          if (mounted) {
            if (widget.lazyPlaylistUrl != null || _episodes.length > 1) {
              if (_autoNext && _currentIndex + 1 < _episodes.length) {
                _playNextEpisode();
              }
            } else {
              Navigator.pop(context);
            }
          }"""
            
    content = re.sub(old_code, new_code, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_pop('lib/screens/player_screen.dart')
