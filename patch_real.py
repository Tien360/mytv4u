import re
path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Import
if "import '../widgets/audio_player_effects.dart';" not in content:
    content = content.replace("import '../widgets/advanced_controls_panel.dart';", "import '../widgets/advanced_controls_panel.dart';\nimport '../widgets/audio_player_effects.dart';")

# 2. Add Getter
bool_getter = """
  bool get _isAudioOnlyFile {
    final url = _currentUrl.toLowerCase();
    if (url.endsWith('.mp3') || url.endsWith('.wav') || url.endsWith('.flac') || url.endsWith('.m4a') || url.endsWith('.aac')) {
      return true;
    }
    if (_videoTracks.isEmpty) return true;
    return _videoTracks.every((t) => t.albumart == true || t.image == true || t.id == 'no-video' || (t.title?.toLowerCase().contains('album art') ?? false));
  }
"""
if "_isAudioOnlyFile" not in content:
    content = content.replace("  bool _isDisposed = false;", "  bool _isDisposed = false;\n" + bool_getter)

# 3. Replace Video
pattern = re.compile(r'child:\s*Video\(\s*controller:\s*controller,')
replacement = r'''child: _isAudioOnlyFile 
                          ? AudioPlayerEffects(
                              player: player,
                              controller: controller,
                              isPlaying: _isPlaying,
                              hasAlbumArt: _videoTracks.isNotEmpty,
                            )
                          : Video(
                              controller: controller,'''

content = pattern.sub(replacement, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESSFULLY Patched player_screen.dart")
