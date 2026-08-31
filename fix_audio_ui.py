import os
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

settings_button = '''          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.pushNamed(context, '/settings').then((_) {
                _loadSettings();
              });
            },
          ),
          IconButton(
'''

content = content.replace('''          IconButton(
            icon: const Icon(Icons.playlist_play),''', settings_button)

# Also fix the .mp3 extension showing in title
content = content.replace("title = file.name;", "title = file.name.replaceAll(RegExp(r'\\.[a-zA-Z0-9]+$'), '');")

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
