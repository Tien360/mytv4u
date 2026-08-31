import re

def refactor_settings(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to replace the layout inside build() method
    # specifically this part:
    # if (_currentUser != null) _buildUserCard() else _buildLoginCard(),
    # const SizedBox(height: 16),
    # _buildYouTubeLinkCard(),
    
    old_layout = r"if \(_currentUser != null\)\s*_buildUserCard\(\)\s*else\s*_buildLoginCard\(\),\s*const SizedBox\(height: 16\),\s*_buildYouTubeLinkCard\(\),"
    new_layout = "_buildUnifiedAccountSection(),"
    
    content = re.sub(old_layout, new_layout, content)
    
    # Now we define _buildUnifiedAccountSection() right after _buildYouTubeLinkCard() definition
    # Wait, let's just append it before Widget _buildSectionTitle
    
    unified_widget = """
  Widget _buildUnifiedAccountSection() {
    final bool isGoogleLinked = _currentUser != null;
    final bool isYtLinked = _isYtLinked;
    
    return GlassContainer(
      padding: const EdgeInsets.all(20),
      borderRadius: 16,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              if (isGoogleLinked && _currentUser!['photoURL']!.isNotEmpty)
                CircleAvatar(
                  radius: 30,
                  backgroundImage: CachedNetworkImageProvider(_currentUser!['photoURL']!),
                )
              else
                CircleAvatar(
                  radius: 30,
                  backgroundColor: Colors.white.withOpacity(0.1),
                  child: Icon(Icons.person, size: 30, color: Colors.white),
                ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      isGoogleLinked ? _currentUser!['displayName']! : L10n.t('login_btn'),
                      style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
                    ),
                    if (isGoogleLinked)
                      Text(
                        _currentUser!['uid']!,
                        style: TextStyle(color: Colors.white.withOpacity(0.5), fontSize: 13),
                      ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),
          Text('TRẠNG THÁI KẾT NỐI:', style: TextStyle(color: Colors.white.withOpacity(0.5), fontSize: 12, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          
          // Google Auth / Firebase
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Icon(Icons.cloud_sync, color: isGoogleLinked ? Colors.blueAccent : Colors.grey, size: 20),
                  const SizedBox(width: 8),
                  Text('Dữ liệu cá nhân trên Firebase', style: TextStyle(color: isGoogleLinked ? Colors.white : Colors.grey)),
                ],
              ),
              if (isGoogleLinked)
                OutlinedButton(
                  onPressed: () async {
                    await AuthApi.logout();
                    setState(() => _currentUser = null);
                  },
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Colors.redAccent,
                    side: const BorderSide(color: Colors.redAccent),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  ),
                  child: const Text('Ngắt kết nối', style: TextStyle(fontSize: 12)),
                )
              else
                ElevatedButton(
                  onPressed: _login,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueAccent,
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  ),
                  child: const Text('Kết nối', style: TextStyle(fontSize: 12, color: Colors.white)),
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
                  Icon(Icons.play_circle_filled, color: isYtLinked ? Colors.redAccent : Colors.grey, size: 20),
                  const SizedBox(width: 8),
                  Text('YouTube (Gợi ý Cá nhân hóa)', style: TextStyle(color: isYtLinked ? Colors.white : Colors.grey)),
                ],
              ),
              if (isYtLinked)
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
                    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(L10n.t('yt_unlink_msg'))));
                  },
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Colors.redAccent,
                    side: const BorderSide(color: Colors.redAccent),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  ),
                  child: const Text('Ngắt kết nối', style: TextStyle(fontSize: 12)),
                )
              else
                ElevatedButton(
                  onPressed: _openYoutubeLogin,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.redAccent,
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  ),
                  child: const Text('Kết nối', style: TextStyle(fontSize: 12, color: Colors.white)),
                ),
            ],
          ),
        ],
      ),
    );
  }
"""

    # We need to insert unified_widget before `Widget _buildSectionTitle`
    content = content.replace("Widget _buildSectionTitle", unified_widget + "\n  Widget _buildSectionTitle")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

refactor_settings('lib/screens/settings_screen.dart')
print("Refactored settings UI successfully!")
