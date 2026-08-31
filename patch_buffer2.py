def patch_buffer_ui_v2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. State
    if "Duration _buffer = Duration.zero;" not in content:
        content = content.replace("Duration _position = Duration.zero;", "Duration _position = Duration.zero;\n  Duration _buffer = Duration.zero;")

    # 2. Listener
    target_listener = '''_playerSubs.add(
      player.stream.position.listen((position) {
        if (mounted) setState(() => _position = position);
      }),
    );'''
    replacement_listener = '''_playerSubs.add(
      player.stream.position.listen((position) {
        if (mounted) setState(() => _position = position);
      }),
    );
    _playerSubs.add(
      player.stream.buffer.listen((buffer) {
        if (mounted) setState(() => _buffer = buffer);
      }),
    );'''
    if "player.stream.buffer.listen" not in content:
        content = content.replace(target_listener, replacement_listener)

    # 3. Slider
    target_slider = '''child: Slider(
                                                    value: _position'''
    replacement_slider = '''child: Slider(
                                                    secondaryTrackValue: _buffer.inMilliseconds.toDouble().clamp(0.0, _duration.inMilliseconds.toDouble() > 0 ? _duration.inMilliseconds.toDouble() : 1.0),
                                                    value: _position'''
    if "secondaryTrackValue" not in content:
        content = content.replace(target_slider, replacement_slider)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_buffer_ui_v2('lib/screens/player_screen.dart')
print("Patched Buffer UI v2")
