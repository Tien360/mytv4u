import re
content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

yt_card = """
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 8),
            child: Divider(color: Colors.white10),
          ),
          // YouTube
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
          ),
"""

if "// YouTube" not in content:
    # Inject before the end of _buildUserCard
    match1 = re.search(r'(Widget _buildUserCard\(\) \{.*?)(\s*\]\,\s*\)\,\s*\)\;\s*\}\s*Future<void> _openYoutubeLogin)', content, re.DOTALL)
    if match1:
        content = content.replace(match1.group(0), match1.group(1) + yt_card + match1.group(2))
        print("Injected into user card")
    
    # Inject before the end of _buildLoginCard
    match2 = re.search(r'(Widget _buildLoginCard\(\) \{.*?)(\s*\]\,\s*\)\,\s*\)\;\s*\}\s*Widget _buildModernSourceCard)', content, re.DOTALL)
    if match2:
        content = content.replace(match2.group(0), match2.group(1) + yt_card + match2.group(2))
        print("Injected into login card")

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
