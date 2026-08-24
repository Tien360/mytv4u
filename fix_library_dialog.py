import re

with open("lib/screens/library_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

new_dialog = """  void _showOpenUrlDialog(BuildContext context) {
    final TextEditingController _urlController = TextEditingController();
    bool _isLive = false;
    showDialog(
      context: context,
      barrierColor: Colors.black.withValues(alpha: 0.6),
      builder: (context) => StatefulBuilder(
        builder: (context, setState) => Dialog(
          backgroundColor: Colors.transparent,
          elevation: 0,
          child: GlassContainer(
            width: 450,
            padding: const EdgeInsets.all(24),
            borderRadius: 24,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Mở đường dẫn mạng (URL)',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 24),
                TextField(
                  controller: _urlController,
                  style: const TextStyle(color: Colors.white),
                  decoration: InputDecoration(
                    hintText: 'Nhập link video/audio (mp4, m3u8, mp3...)',
                    hintStyle: const TextStyle(color: Colors.white30),
                    filled: true,
                    fillColor: Colors.black.withValues(alpha: 0.2),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: const BorderSide(color: Colors.blueAccent),
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                InkWell(
                  onTap: () => setState(() => _isLive = !_isLive),
                  borderRadius: BorderRadius.circular(8),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 4.0),
                    child: Row(
                      children: [
                        Icon(
                          _isLive ? Icons.check_circle : Icons.circle_outlined,
                          color: _isLive ? Colors.blueAccent : Colors.white54,
                          size: 24,
                        ),
                        const SizedBox(width: 12),
                        const Text(
                          'Đánh dấu là luồng trực tiếp (Live)',
                          style: TextStyle(color: Colors.white, fontSize: 16),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 32),
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      style: TextButton.styleFrom(
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                      ),
                      child: const Text('Hủy', style: TextStyle(color: Colors.white54, fontSize: 16)),
                    ),
                    const SizedBox(width: 12),
                    ElevatedButton(
                      onPressed: () {
                        final url = _urlController.text.trim();
                        if (url.isNotEmpty) {
                          Navigator.pop(context);
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => PlayerScreen(
                                episodes: [
                                  Episode(
                                    name: 'Stream',
                                    slug: 'stream',
                                    m3u8Url: url,
                                    embedUrl: '',
                                  ),
                                ],
                                currentEpisodeIndex: 0,
                                movieName: 'Luồng Mạng',
                                isLive: _isLive,
                              ),
                            ),
                          );
                        }
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blueAccent,
                        padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: const Text('Mở', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }"""

text = re.sub(r'  void _showOpenUrlDialog\(BuildContext context\) \{.*?\n  \}\n', new_dialog + '\n', text, flags=re.DOTALL)
with open("lib/screens/library_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
print("Replaced _showOpenUrlDialog!")
