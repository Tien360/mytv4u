import re
path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update hasAlbumArt logic and pass duration
old_audio_effects = """                              player: player,
                              controller: controller,
                              isPlaying: _isPlaying,
                              hasAlbumArt: _videoTracks.isNotEmpty,
                            )"""

new_audio_effects = """                              player: player,
                              controller: controller,
                              isPlaying: _isPlaying,
                              hasAlbumArt: _videoTracks.any((t) => t.albumart == true || t.image == true || (t.title?.toLowerCase().contains('album art') ?? false)),
                              duration: _duration,
                            )"""
content = content.replace(old_audio_effects, new_audio_effects)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated player_screen.dart AudioPlayerEffects call")
