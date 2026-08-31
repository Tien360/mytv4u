import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State Variables
var_search = "bool _defaultRepeat = false;"
var_inject = "bool _defaultRepeat = false;\n  String _ytCookieSource = 'none';\n"
content = content.replace(var_search, var_inject)

# 2. Load
load_search = "_easterEggsEnabled = _prefs!.getBool('enable_easter_eggs') ?? true;"
load_inject = "_easterEggsEnabled = _prefs!.getBool('enable_easter_eggs') ?? true;\n    _ytCookieSource = _prefs!.getString('yt_cookie_source') ?? 'none';"
content = content.replace(load_search, load_inject)

# 3. UI
ui_inject = """  Widget _buildYouTubeLinkCard() {
    return Container(
      margin: const EdgeInsets.only(top: 24),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.05),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.video_library, color: Colors.redAccent, size: 28),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Liên kết YouTube (Đồng bộ thuật toán)',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Giúp app đọc được "My Mix" và gợi ý video chuẩn xác như bạn đang xem trên web bằng cách mượn Cookies từ trình duyệt.',
                      style: TextStyle(color: Colors.white.withValues(alpha: 0.6)),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),
          Row(
            children: [
              const Text('Nguồn Cookies:', style: TextStyle(color: Colors.white70)),
              const SizedBox(width: 16),
              Expanded(
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<String>(
                    dropdownColor: const Color(0xFF1E1E1E),
                    value: _ytCookieSource,
                    isExpanded: true,
                    style: const TextStyle(color: Colors.white, fontSize: 16),
                    items: const [
                      DropdownMenuItem(value: 'none', child: Text('Không liên kết (Ẩn danh)')),
                      DropdownMenuItem(value: 'chrome', child: Text('Nhập từ Google Chrome')),
                      DropdownMenuItem(value: 'edge', child: Text('Nhập từ Microsoft Edge')),
                      DropdownMenuItem(value: 'firefox', child: Text('Nhập từ Mozilla Firefox')),
                      DropdownMenuItem(value: 'brave', child: Text('Nhập từ Brave')),
                      DropdownMenuItem(value: 'opera', child: Text('Nhập từ Opera')),
                    ],
                    onChanged: (val) async {
                      if (val != null) {
                        setState(() {
                          _ytCookieSource = val;
                        });
                        final p = await SharedPreferences.getInstance();
                        await p.setString('yt_cookie_source', val);
                        if (mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text(val == 'none' ? 'Đã tắt liên kết YouTube' : 'Đã chọn liên kết qua trình duyệt $val'),
                              backgroundColor: Colors.green,
                            ),
                          );
                        }
                      }
                    },
                  ),
                ),
              ),
            ],
          ),
          if (_ytCookieSource != 'none') ...[
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.orange.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.orange.withValues(alpha: 0.3)),
              ),
              child: const Row(
                children: [
                  Icon(Icons.warning_amber_rounded, color: Colors.orange, size: 20),
                  SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      'Lưu ý: Nếu trình duyệt của bạn bảo mật cao (chặn chia sẻ tệp), hãy tắt hẳn trình duyệt đi trước khi mở video YouTube trong app nhé.',
                      style: TextStyle(color: Colors.orange, fontSize: 13),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

"""
idx = content.find("Widget _buildUserCard()")
content = content[:idx] + ui_inject + content[idx:]

account_search = """                                  if (_currentUser != null)
                                    _buildUserCard()
                                  else
                                    _buildLoginCard(),"""
account_inject = account_search + "\n\n                                  _buildYouTubeLinkCard(),"
content = content.replace(account_search, account_inject)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched settings_screen.dart")
