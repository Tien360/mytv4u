path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We want to replace from "  Future<bool> _prompt8KCinemaMode" to the end of "_changeYtQuality"
original_change = """  void _changeYtQuality(int height) async {
    setState(() => _selectedYtHeight = height);
    final formatStr = height == 0
        ? 'bestvideo[vcodec!*=av01]+bestaudio/bestvideo+bestaudio/best'
        : 'bestvideo[vcodec!*=av01][height<=$height]+bestaudio/bestvideo[height<=$height]+bestaudio/best';
    try {
      (player.platform as dynamic).setProperty('ytdl-format', formatStr);
    } catch (_) {}

    final pos = player.state.position;
    await player.open(Media(_currentUrl));
    if (pos > Duration.zero) {
      await player.seek(pos);
    }
  }"""

pattern = r"  Future<bool> _prompt8KCinemaMode\(int height\) async \{.*?  void _changeYtQuality\(int height\) async \{.*?  \}"
content = re.sub(pattern, original_change, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Reverted!")
