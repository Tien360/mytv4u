with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

import re

old_yt_row2 = """            // YouTube
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    Icon(Icons.play_circle_filled, color: _isYtLinked ? Colors.redAccent : Colors.grey, size: 20),
                    const SizedBox(width: 8),
                    Text(L10n.t('sync_yt') ?? 'YouTube (Gợi ý Cá nhân hóa)', style: TextStyle(color: _isYtLinked ? Colors.white : Colors.grey)),
                  ],
                ),
                if (_isYtLinked)
                  OutlinedButton(
                    onPressed: () async {
                      final prefs = await SharedPreferences.getInstance();
                      await prefs.setBool('is_yt_linked', false);
                      setState(() => _isYtLinked = false);
                      
                      try {
                        final exeName = File(Platform.resolvedExecutable).uri.pathSegments.last.replaceAll('.exe', '');
                        final defaultWebviewPath = '${Platform.environment['LOCALAPPDATA']}\\\\flutter_webview_windows\\\\${exeName}\\\\EBWebView';
                        final dir = Directory(defaultWebviewPath);
                        if (dir.existsSync()) {
                          dir.deleteSync(recursive: true);
                        }
                      } catch (e) {
                        debugPrint('Failed to delete WebView data: $e');
                      }
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(L10n.t('yt_unlink_msg') ?? 'Đã ngắt kết nối YouTube')));
                    },
                    style: OutlinedButton.styleFrom(
                      foregroundColor: Colors.redAccent,
                      side: const BorderSide(color: Colors.redAccent),
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    ),
                    child: Text(L10n.t('btn_disconnect') ?? 'Ngắt kết nối', style: const TextStyle(fontSize: 12)),
                  )
                else
                  ElevatedButton(
                    onPressed: _openYoutubeLogin,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.redAccent,
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    ),
                    child: Text(L10n.t('btn_connect') ?? 'Kết nối', style: const TextStyle(fontSize: 12, color: Colors.white)),
                  ),
              ],
            ),"""

new_yt_row2 = """            // YouTube
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: _isYtLinked ? Colors.redAccent.withOpacity(0.1) : Colors.white10,
                    shape: BoxShape.circle,
                  ),
                  child: Icon(Icons.smart_display, color: _isYtLinked ? Colors.redAccent : Colors.grey, size: 24),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Text(
                    L10n.t('sync_yt') ?? 'YouTube (Gợi ý Cá nhân hóa)', 
                    style: TextStyle(
                      color: _isYtLinked ? Colors.white : Colors.grey,
                      fontSize: 16,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
                if (_isYtLinked)
                  OutlinedButton.icon(
                    onPressed: () async {
                      final prefs = await SharedPreferences.getInstance();
                      await prefs.setBool('is_yt_linked', false);
                      setState(() => _isYtLinked = false);
                      try {
                        final exeName = File(Platform.resolvedExecutable).uri.pathSegments.last.replaceAll('.exe', '');
                        final defaultWebviewPath = '${Platform.environment['LOCALAPPDATA']}\\\\flutter_webview_windows\\\\${exeName}\\\\EBWebView';
                        final dir = Directory(defaultWebviewPath);
                        if (dir.existsSync()) {
                          dir.deleteSync(recursive: true);
                        }
                      } catch (e) {}
                    },
                    icon: const Icon(Icons.link_off, size: 18),
                    label: Text(L10n.t('btn_disconnect') ?? 'Ngắt kết nối'),
                    style: OutlinedButton.styleFrom(
                      foregroundColor: Colors.redAccent,
                      side: const BorderSide(color: Colors.redAccent),
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  )
                else
                  ElevatedButton.icon(
                    onPressed: _openYoutubeLogin,
                    icon: const Icon(Icons.link, size: 18),
                    label: Text(L10n.t('btn_connect') ?? 'Kết nối'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.redAccent,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  ),
              ],
            ),"""

# Need to replace exactly the old text but ignoring encoding weirdness
match2 = re.search(r'(\s*// YouTube\s*Row\(\s*mainAxisAlignment: MainAxisAlignment.spaceBetween,\s*children: \[.*?ElevatedButton\(.*?btn_connect.*?\}\,\s*\)\,\s*\]\,\s*\)\,\s*)', content, re.DOTALL)
if match2:
    content = content.replace(match2.group(1), new_yt_row2 + "\n")
    print("Replaced login card")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
