with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

bad_str = """      player.stream.error.listen((error) {
        if (mounted) {
          if (_tryFallbackDomain()) return;
          setState(() => errorMsg = error.toString());
        }
      }),"""

good_str = """      player.stream.error.listen((error) {
        if (mounted) {
          String errStr = error.toString();
          if (errStr.contains('ffurl_read') || errStr.contains('0xdfb9b0bb') || errStr.contains('tcp:')) {
            return; // Bỏ qua cảnh báo gián đoạn mạng tạm thời không gây crash
          }
          if (_tryFallbackDomain()) return;
          setState(() => errorMsg = errStr);
        }
      }),"""

if bad_str in content:
    content = content.replace(bad_str, good_str)
    with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced error listener")
else:
    print("Could not find block")
