with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

user_card_text = """  Widget _buildUserCard() {
    if (_currentUser == null) return const SizedBox.shrink();
    return GlassContainer(
      padding: const EdgeInsets.all(20),
      borderRadius: 16,
      child: Column(
        children: [
          Row(
            children: [
              CircleAvatar(
                radius: 36,
                backgroundImage: _currentUser!['photoURL']!.isNotEmpty
                    ? CachedNetworkImageProvider(_currentUser!['photoURL']!)
                    : null,
                child: _currentUser!['photoURL']!.isEmpty
                    ? const Icon(Icons.person, size: 36)
                    : null,
              ),
              const SizedBox(width: 20),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _currentUser!['displayName']!,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 10,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.green.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.green.withOpacity(0.5)),
                      ),
                      child: Text(
                        L10n.t('synced_with_web'),
                        style: TextStyle(
                          color: Colors.greenAccent,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              OutlinedButton.icon(
                onPressed: _handleLogout,
                icon: const Icon(Icons.logout, size: 18),
                label: Text(L10n.t('logout')),
                style: OutlinedButton.styleFrom(
                  foregroundColor: Colors.redAccent,
                  side: const BorderSide(color: Colors.redAccent),
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ],
          ),
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
                    } catch (e) {}
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
        ],
      ),
    );
  }"""

import re
match = re.search(r'(Widget _buildUserCard\(\) \{.*?)(\s*Future<void> _openYoutubeLogin)', content, re.DOTALL)
if match:
    content = content.replace(match.group(1), user_card_text + "\n\n")
    print("Replaced user card")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
