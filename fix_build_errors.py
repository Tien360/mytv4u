import re
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# Fix _initPlayer to _loadCurrent
content = content.replace('_initPlayer();', '_loadCurrent();')

# Fix AudioVisualizer missing isPlaying
content = content.replace("AudioVisualizer(type: 'inline', color: _dominantColor)", "AudioVisualizer(isPlaying: isPlaying, type: 'inline', color: _dominantColor)")

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
