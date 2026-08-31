import sys

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# For _buildUserCard
old_yt1 = """          // YouTube
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Icon(Icons.play_circle_filled, color: _isYtLinked ? Colors.redAccent : Colors.grey, size: 20),
                  const SizedBox(width: 8),
                  Text(L10n.t('sync_yt') ?? 'YouTube (G?i y C nhn ha)', style: TextStyle(color: _isYtLinked ? Colors.white : Colors.grey)),
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
                    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(L10n.t('yt_unlink_msg') ?? 'Da ng?t k?t n?i YouTube')));
                  },
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Colors.redAccent,
                    side: const BorderSide(color: Colors.redAccent),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  ),
                  child: Text(L10n.t('btn_disconnect') ?? 'Ng?t k?t n?i', style: const TextStyle(fontSize: 12)),
                )
              else
                ElevatedButton(
                  onPressed: _openYoutubeLogin,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.redAccent,
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  ),
                  child: Text(L10n.t('btn_connect') ?? 'K?t n?i', style: const TextStyle(fontSize: 12, color: Colors.white)),
                ),
            ],
          ),"""

new_yt1 = """          // YouTube
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

# Because of charset encoding, I'll use regex but EXACTLY matching `// YouTube` to the closing `Row`

import re
match = re.search(r'(          // YouTube\s*Row\(\s*mainAxisAlignment: MainAxisAlignment.spaceBetween,\s*children: \[.*?ElevatedButton\(.*?\}\,\s*\)\,\s*\]\,\s*\)\,)', content, re.DOTALL)
if match:
    # There should be TWO matches (one in _buildUserCard, one in _buildLoginCard)
    matches = list(re.finditer(r'(          // YouTube\s*Row\(\s*mainAxisAlignment: MainAxisAlignment.spaceBetween,\s*children: \[.*?ElevatedButton\(.*?\}\,\s*\)\,\s*\]\,\s*\)\,)', content, re.DOTALL))
    print(f"Found {len(matches)} YouTube rows")
    
    # Replace from back to front to avoid shifting indices
    for m in reversed(matches):
        content = content[:m.start()] + new_yt1 + content[m.end():]
    
    with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("Could not find YouTube row to replace!")
