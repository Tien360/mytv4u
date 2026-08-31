import sys

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

new_yt_row2 = """          // YouTube
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
          ),
        ],
      ),
    );
  }

"""

start_idx = content.find("          // YouTube", 72000)
end_idx = content.find("  Widget _buildModernSourceCard", start_idx)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_yt_row2 + content[end_idx:]
    print("Replaced LoginCard YouTube row successfully using exact indexing!")
else:
    print(f"Could not find start or end index! {start_idx} {end_idx}")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
