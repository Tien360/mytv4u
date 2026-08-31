import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

func = """  void _openInWebPlayer() async {
    player.pause();
    if (mounted) {
      setState(() {
        _isExternalPlayerActive = true;
      });
    }
    try {
      final bounds = await windowManager.getBounds();
      final title = "${widget.movieName} - YouTube";
      final exeDir = File(Platform.resolvedExecutable).parent.path;
      var exePath = '$exeDir\\\\tv_web_player.exe';
      if (!File(exePath).existsSync()) {
        exePath = r"T:\Project\Phim\tv_web_player\bin\Release\net8.0-windows\tv_web_player.exe";
      }

      String targetUrl = widget.lazyPlaylistUrl ?? _currentUrl;

      List<String> args = [
        targetUrl,
        title,
        bounds.left.toInt().toString(),
        bounds.top.toInt().toString(),
        bounds.width.toInt().toString(),
        bounds.height.toInt().toString(),
      ];

      final process = await Process.start(exePath, args);
      await process.exitCode;

      if (mounted) {
        setState(() => _isExternalPlayerActive = false);
      }
    } catch (e) {
      debugPrint('Error launching web player: $e');
    }
  }

  Future<void> _playCurrentUrl(Episode ep) async {"""
content = content.replace("  Future<void> _playCurrentUrl(Episode ep) async {", func)

button_code = """                                                if (_isYoutube) ...[
                                                  IconButton(
                                                    icon: const Icon(
                                                      Icons.open_in_browser,
                                                      color: Colors.white,
                                                      size: 20,
                                                    ),
                                                    onPressed: _openInWebPlayer,
                                                    tooltip: 'Mở bằng Web Player (Tối ưu 8K/4K)',
                                                    padding: const EdgeInsets.all(4),
                                                    constraints: const BoxConstraints(),
                                                  ),
                                                  const SizedBox(width: 10),
                                                ],
                                                // Settings Gear Button"""
content = content.replace("                                                // Settings Gear Button", button_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated player_screen.dart")
