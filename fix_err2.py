with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

bad_str = """    _playerSubs.add(
      player.stream.playing.listen((playing) {
        if (mounted) setState(() => _isPlaying = playing);
      }),
    );"""

good_str = """    _playerSubs.add(
      player.stream.playing.listen((playing) {
        if (mounted) {
          setState(() {
            _isPlaying = playing;
            if (playing && errorMsg != null) {
              errorMsg = null; // Auto-dismiss error if video starts playing
            }
          });
        }
      }),
    );"""

if bad_str in content:
    content = content.replace(bad_str, good_str)
    with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("Injected auto-dismiss")
else:
    print("Could not find playing listener")
