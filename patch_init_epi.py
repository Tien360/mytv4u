import re
with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

pattern = r"if \(_currentUrl\.startsWith\('premium://'\)\) \{[\s\S]*?print\(\"Premium resolver error: \$e\"\);\s*\}\s*\}"

new_code = """if (_currentUrl.startsWith('premium://')) {
        String rawId = '';
        final uri = Uri.tryParse(_currentUrl); if (uri == null) return; rawId = uri.pathSegments.last;
        _premiumRawId = rawId;
        try {
            final streams = await PremiumResolver.getVideoStream(rawId);
            if (streams.isNotEmpty) {
                _premiumStreams = streams;
                _currentUrl = streams.first;
            } else {
                if (mounted) setState(() => errorMsg = "Không tìm thấy luồng Premium/Free2 khả dụng.");
                return;
            }
        } catch (e) {
            print("Premium resolver error: $e");
            if (mounted) setState(() => errorMsg = "Máy chủ Premium/Free2 bị quá tải hoặc từ chối kết nối.");
            return;
        }
    }"""

text, count = re.subn(pattern, new_code, text)
print(f"Replaced {count} times")

with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
