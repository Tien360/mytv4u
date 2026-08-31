import sys

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

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

idx1 = content.find("          // YouTube")
if idx1 != -1:
    end_idx1 = content.find("        ],\n      ),\n    );\n  }\n  \n  \n  Future<void> _openYoutubeLogin", idx1)
    if end_idx1 != -1:
        content = content[:idx1] + new_yt1 + "\n" + content[end_idx1:]
        print("Replaced YouTube row in user card!")
    else:
        end_idx1 = content.find("  Future<void> _openYoutubeLogin", idx1)
        # backtrack to the closing brackets
        # The closing brackets are `        ],\n      ),\n    );\n  }\n`
        # which is 33 chars long. But I'll just use regex to find the end safely.
        import re
        match = re.search(r'(\s*\]\,\s*\)\,\s*\)\;\s*\}\s*Future<void> _openYoutubeLogin)', content[idx1:])
        if match:
            content = content[:idx1] + new_yt1 + match.group(1) + content[idx1 + match.end():]
            print("Replaced YouTube row in user card with fallback regex!")
        else:
            print("Still could not find end of user card")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
