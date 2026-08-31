path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find the location to insert the dialog method
dialog_code = """
  Future<bool> _prompt8KCinemaMode(int height) async {
    final bool wasPlaying = player.state.playing;
    if (wasPlaying) player.pause();
    
    final result = await showDialog<bool>(
      context: context,
      barrierColor: Colors.black.withOpacity(0.7),
      builder: (context) {
        return Center(
          child: Material(
            color: Colors.transparent,
            child: GlassContainer(
              width: 400,
              padding: const EdgeInsets.all(24),
              borderRadius: BorderRadius.circular(20),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.movie_creation_rounded, color: Colors.blueAccent, size: 64),
                  const SizedBox(height: 16),
                  Text(
                    'Chế độ UltraHD (${height}p)',
                    style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'Phát nội dung 4K/8K yêu cầu phần cứng rất cao. Ứng dụng sẽ tự động chuyển sang trình phát MPV Toàn màn hình để tối ưu 100% sức mạnh GPU (Chống lag tuyệt đối).\n\nBạn có thể điều khiển tua, âm lượng bằng thanh công cụ gốc của MPV.\n\nNhấn phím ESC để trở về.',
                    style: TextStyle(color: Colors.white70, fontSize: 15, height: 1.5),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 24),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      TextButton(
                        onPressed: () => Navigator.pop(context, false),
                        child: const Text('Hủy bỏ', style: TextStyle(color: Colors.white54)),
                      ),
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.blueAccent,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                        ),
                        onPressed: () => Navigator.pop(context, true),
                        child: const Text('Đồng ý', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
    return result ?? false;
  }

"""

# Insert dialog code before _changeYtQuality
content = content.replace("  void _changeYtQuality", dialog_code + "  void _changeYtQuality")

new_change = """  void _changeYtQuality(int height) async {
    if (height >= 2160 && Platform.isWindows) {
      final proceed = await _prompt8KCinemaMode(height);
      if (!proceed) return;
    }

    setState(() => _selectedYtHeight = height);
    final formatStr = height == 0
        ? 'bestvideo[vcodec!*=av01]+bestaudio/bestvideo+bestaudio/best'
        : 'bestvideo[vcodec!*=av01][height<=$height]+bestaudio/bestvideo[height<=$height]+bestaudio/best';
    try {
      final platform = player.platform as dynamic;
      platform.setProperty('ytdl-format', formatStr);
      
      // If 4K/8K, enable MPV full cinema mode
      if (height >= 2160 && Platform.isWindows) {
        platform.setProperty('vo', 'gpu-next');
        platform.setProperty('gpu-api', 'd3d11');
        platform.setProperty('osc', 'yes');
        platform.setProperty('fullscreen', 'yes');
        platform.setProperty('title', 'MyTV4U UltraHD Cinema');
      } else if (Platform.isWindows) {
        platform.setProperty('vo', ''); // Reset to default texture mode
        platform.setProperty('osc', 'no');
      }
    } catch (_) {}

    final pos = player.state.position;
    await player.open(Media(_currentUrl));
    if (pos > Duration.zero) {
      await player.seek(pos);
    }
    player.play();
  }"""

# Replace the original _changeYtQuality
content = re.sub(r'  void _changeYtQuality\(int height\) async \{.*?\n  \}', new_change, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully")
