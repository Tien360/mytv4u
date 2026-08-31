import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """          // Go back to previous screen automatically when player is closed
          if (mounted) {
            if (widget.lazyPlaylistUrl != null || _episodes.length > 1) {
              if (_autoNext && _currentIndex + 1 < _episodes.length) {
                _playNextEpisode();
              }
            } else {
              Navigator.pop(context);
            }
          }"""

new_logic = """          // Go back to previous screen automatically when player is closed
          if (mounted) {
            Navigator.pop(context);
          }"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced logic in player_screen.dart successfully")
else:
    print("Could not find old_logic in player_screen.dart")
