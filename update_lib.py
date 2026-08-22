import re

with open('lib/screens/library_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix allowedExtensions
new_exts = """
                            'mp4',
                            'mkv',
                            'avi',
                            'flv',
                            'webm',
                            'mov',
                            'ts',
                            'mp3',
                            'm4a',
                            'wav',
                            'flac',
                            'aac',
"""

content = re.sub(r"\'mp4\',\s*\'mkv\',\s*\'avi\',\s*\'flv\',\s*\'webm\',\s*\'mov\',\s*\'ts\',", new_exts, content)

# Add "Open URL" button
open_url_button = r"""
                  Row(
                    children: [
                      ElevatedButton.icon(
                        icon: const Icon(Icons.link, color: Colors.white),
                        label: const Text(
                          'Mở Link',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white.withAlpha(25),
                          padding: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 14,
                          ),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(24),
                          ),
                        ),
                        onPressed: () {
                          _showOpenUrlDialog(context);
                        },
                      ),
                      const SizedBox(width: 12),
                      ElevatedButton.icon(
                        icon: const Icon(Icons.folder_open, color: Colors.white),
                        label: const Text(
                          'Mở File',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white.withAlpha(25),
                          padding: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 14,
                          ),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(24),
                          ),
                        ),
                        onPressed: () async {
"""

content = re.sub(r'ElevatedButton\.icon\(\s*icon: const Icon\(Icons\.folder_open, color: Colors\.white\),\s*label: const Text\(\s*\'Mở file trên máy\'.*?onPressed: \(\) async \{', open_url_button, content, flags=re.DOTALL)

# Add the dialog method at the end of the class
dialog_method = r"""
  void _showOpenUrlDialog(BuildContext context) {
    final TextEditingController _urlController = TextEditingController();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2C),
        title: const Text('Mở đường dẫn mạng (URL)', style: TextStyle(color: Colors.white)),
        content: TextField(
          controller: _urlController,
          style: const TextStyle(color: Colors.white),
          decoration: const InputDecoration(
            hintText: 'Nhập link video/audio (mp4, m3u8, mp3...)',
            hintStyle: TextStyle(color: Colors.white54),
            enabledBorder: UnderlineInputBorder(
              borderSide: BorderSide(color: Colors.white24),
            ),
            focusedBorder: UnderlineInputBorder(
              borderSide: BorderSide(color: Colors.blueAccent),
            ),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Hủy', style: TextStyle(color: Colors.white54)),
          ),
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
                      movieName: 'Network Stream',
                    ),
                  ),
                );
              }
            },
            style: ElevatedButton.styleFrom(backgroundColor: Colors.blueAccent),
            child: const Text('Mở', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }
}
"""

content = re.sub(r'\}\s*\}$', dialog_method, content)

with open('lib/screens/library_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated library_screen.dart")
