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

# Find where to inject in _buildUserCard
# Usually it's after the synced_with_web or btn_disconnect
if "// YouTube" not in content:
    # use regex to inject right before the end of the Expanded Column in _buildUserCard
    # which is right before:
    #             ],
    #           ),
    #         ),
    #       ],
    #     ),
    #   );
    user_match = re.search(r'(L10n\.t\(\'btn_disconnect\'\).*?\)\s*\]\,\s*\)\,\s*\)\,\s*\]\,\s*\)\,\s*\)\;)', content, re.DOTALL)
    if user_match:
        content = content.replace(user_match.group(1), user_match.group(1).replace("],\n              ),\n            ),", yt_card + "\n              ],\n              ),\n            ),"))
    
    # Login card: inject right after the ElevatedButton for login_google
    login_match = re.search(r'(elevation\: 4\,\s*\)\,\s*\)\,\s*\]\,\s*\)\,\s*\)\;)', content, re.DOTALL)
    if login_match:
        content = content.replace(login_match.group(1), login_match.group(1).replace("],\n        ),\n      );", yt_card + "\n          ],\n        ),\n      );"))

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
print("Injected yt_card!")
