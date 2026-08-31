import codecs

with codecs.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

old_listener = """    _playerSubs.add(
      player.stream.error.listen((error) {
        if (mounted) {
          String errStr = error.toString();
          if (errStr.contains('ffurl_read') || errStr.contains('0xdfb9b0bb') || errStr.contains('tcp:')) {
            return; // Bỏ qua cảnh báo gián đoạn mạng tạm thời không gây crash
          }
          if (_tryFallbackDomain()) return;
          setState(() => errorMsg = errStr);
        }
      }),
    );"""

new_listener = """    _playerSubs.add(
      player.stream.error.listen((error) {
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
                  content: Text('Luồng bị lỗi phần cứng, đang chuyển sang giải mã bằng phần mềm...'),
                  backgroundColor: Colors.orange,
                  duration: Duration(seconds: 3),
                ),
              );
              return;
            } else {
              return; // Bỏ qua không hiển thị lỗi đỏ chót giữa màn hình, để app cố gắng phát tiếp
            }
          }
          if (_tryFallbackDomain()) return;
          setState(() => errorMsg = errStr);
        }
      }),
    );"""

code = code.replace(old_listener, new_listener)

with codecs.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched error listener.")
