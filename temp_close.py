import re
content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()

old_code = """          if (isNearEnd) {
            _playNextEpisode();
          } else {"""

new_code = """          if (isNearEnd) {
            if (_currentIndex + 1 < _episodes.length) {
              _playNextEpisode();
            } else {
              if (mounted) Navigator.pop(context);
            }
          } else {"""

content = content.replace(old_code, new_code)
open('lib/screens/player_screen.dart', 'w', encoding='utf-8').write(content)
