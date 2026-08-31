with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 1. Fix UserCard YouTube Row
# Currently it's a Row inside a Column inside _buildUserCard
old_yt_row = """          Row(
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
          ),"""

new_yt_row = """          Row(
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

if old_yt_row in content:
    content = content.replace(old_yt_row, new_yt_row)
else:
    print("Could not find old yt row!")

# 2. Fix Video Settings Translations
# Subtitle for background_playback
content = content.replace(
    "Text('Tiếp tục phát âm thanh khi ẩn ứng dụng', style: const TextStyle(color: Colors.white54, fontSize: 13))",
    "Text(L10n.t('background_playback_sub') ?? 'Tiếp tục phát âm thanh khi ẩn ứng dụng', style: const TextStyle(color: Colors.white54, fontSize: 13))"
)

# default_speed
content = content.replace(
    "Text('Tốc độ mặc định (Default Speed)', style: const TextStyle(color: Colors.white, fontSize: 16))",
    "Text(L10n.t('default_speed') ?? 'Tốc độ mặc định (Default Speed)', style: const TextStyle(color: Colors.white, fontSize: 16))"
)

# enable_hw_accel
content = content.replace(
    "Text(L10n.t('enable_hw_accel') ?? 'Tng t`c ph n ccng (HW \nAcceleration)', style: const TextStyle(color: Colors.white))",
    "Text(L10n.t('enable_hw_accel') ?? 'Tăng tốc phần cứng (HW Acceleration)', style: const TextStyle(color: Colors.white))"
).replace(
    "Text(L10n.t('enable_hw_accel_sub') ?? 'S dng GPU ` \ngii mA video, gim ti CPU vA tit kim pin.', style: const TextStyle(color: Colors.white54, fontSize: \n13))",
    "Text(L10n.t('enable_hw_accel_sub') ?? 'Sử dụng GPU để giải mã video, giảm tải CPU và tiết kiệm pin.', style: const TextStyle(color: Colors.white54, fontSize: 13))"
)

# And fix any weird UTF-8 characters that might have occurred from powershell pipes earlier
content = content.replace('Tng t`c ph n ccng (HW \nAcceleration)', 'Tăng tốc phần cứng (HW Acceleration)')
content = content.replace('S dng GPU ` \ngii mA video, gim ti CPU vA tit kim pin.', 'Sử dụng GPU để giải mã video, giảm tải CPU và tiết kiệm pin.')

# Just use regex to fix hw_accel text in case of slight variance
content = re.sub(
    r"Text\(L10n\.t\('enable_hw_accel'\).*?style: const TextStyle\(color: Colors\.white\)\)",
    "Text(L10n.t('enable_hw_accel') ?? 'Giải mã bằng phần cứng (HW Decoding)', style: const TextStyle(color: Colors.white))",
    content,
    flags=re.DOTALL
)

content = re.sub(
    r"Text\(L10n\.t\('enable_hw_accel_sub'\).*?style: const TextStyle\(color: Colors\.white54, fontSize:\s*13\)\)",
    "Text(L10n.t('enable_hw_accel_sub') ?? 'Sử dụng GPU để giải mã video, giảm tải CPU và tiết kiệm pin.', style: const TextStyle(color: Colors.white54, fontSize: 13))",
    content,
    flags=re.DOTALL
)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated UI and Translations")
