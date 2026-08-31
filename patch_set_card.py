import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace _buildYouTubeLinkCard
search_start = "Widget _buildYouTubeLinkCard() {"
search_end = "Widget _buildUserCard() {"
idx_start = content.find(search_start)
idx_end = content.find(search_end)

new_card = """Widget _buildYouTubeLinkCard() {
    return Card(
      color: Colors.white.withAlpha(10),
      margin: const EdgeInsets.only(bottom: 24),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.video_library, color: Colors.redAccent, size: 28),
                const SizedBox(width: 12),
                const Text(
                  'Liên kết YouTube (Đồng bộ thuật toán)',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            const Text(
              'Lấy đúng 100% danh sách nhạc từ "My Mix" và các playlist cá nhân hóa bằng cách cấp phiên đăng nhập an toàn.',
              style: TextStyle(color: Colors.white70, fontSize: 14),
            ),
            const SizedBox(height: 24),
            
            if (!_isYtLinked)
              Container(
                width: double.infinity,
                child: ElevatedButton.icon(
                  icon: const Icon(Icons.login, color: Colors.white),
                  label: const Text('Mở Trình duyệt Ẩn để Đăng nhập YouTube', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueAccent,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: _openYoutubeLogin,
                ),
              )
            else
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.green.withAlpha(20),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.green.withAlpha(50)),
                ),
                child: Column(
                  children: [
                    const Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.check_circle, color: Colors.green, size: 24),
                        SizedBox(width: 8),
                        Text('Đã liên kết thành công!', style: TextStyle(color: Colors.green, fontSize: 16, fontWeight: FontWeight.bold)),
                      ],
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton.icon(
                      icon: const Icon(Icons.link_off, color: Colors.white),
                      label: const Text('Ngắt kết nối', style: TextStyle(color: Colors.white)),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.redAccent,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                      ),
                      onPressed: () async {
                        final appDataDir = await getApplicationSupportDirectory();
                        final profileDir = p.join(appDataDir.path, 'youtube_webview_profile');
                        try {
                          await WebviewController.initializeEnvironment(userDataPath: profileDir);
                        } catch(e) {}
                        final _c = WebviewController();
                        await _c.initialize();
                        await _c.clearCookies();
                        await _c.dispose();
                        
                        await _prefs!.setBool('is_yt_linked', false);
                        setState(() { _isYtLinked = false; });
                      },
                    ),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  """

content = content[:idx_start] + new_card + content[idx_end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched _buildYouTubeLinkCard")
