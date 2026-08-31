import codecs

with codecs.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

bad_hw = """        player.stream.error.listen((error) {
          if (mounted) {
            String errStr = error.toString();
            if (errStr.contains('ffurl_read') || errStr.contains('0xdfb9b0bb') || errStr.contains('tcp:')) {
              return; // Bỏ qua cảnh báo gián đoạn mạng tạm thời không gây crash
            }
            if (errStr.toLowerCase().contains('error decoding')) {
              if (_hwAccel) {
                _toggleHwAccel(false);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Phát hiện lỗi phần cứng, đang chuyển sang giải mã bằng phần mềm...'),
                    backgroundColor: Colors.orange,
                    duration: Duration(seconds: 3),
                  ),
                );
                return;
              } else {
                return; // Ignore if already SW decoding
              }
            }
            if (_tryFallbackDomain()) return;
            setState(() => errorMsg = errStr);
          }
        }),"""
good_hw = """        player.stream.error.listen((error) {
          if (mounted) {
            String errStr = error.toString();
            if (errStr.contains('ffurl_read') || errStr.contains('0xdfb9b0bb') || errStr.contains('tcp:')) {
              return; // Bỏ qua cảnh báo gián đoạn mạng tạm thời không gây crash
            }
            if (_tryFallbackDomain()) return;
            setState(() => errorMsg = errStr);
          }
        }),"""
code = code.replace(bad_hw, good_hw)

with codecs.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("Removed auto HW fallback in player_screen.")
