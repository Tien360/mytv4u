import re

def add_buffer_ui(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add _buffer state
    content = content.replace("Duration _position = Duration.zero;", "Duration _position = Duration.zero;\n  Duration _buffer = Duration.zero;")

    # 2. Add listener
    pattern_listener = r"_playerSubs\.add\(\s*player\.stream\.position\.listen\(\(position\) \{\s*if \(mounted\)\s*setState\(\(\) => _position = position\);\s*\}\),\s*\);"
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
    content = re.sub(pattern_listener, replacement_listener, content)

    # 3. Add secondaryTrackValue to Slider
    pattern_slider = r"(child: Slider\(\s*value: _position\s*\.inMilliseconds\s*\.toDouble\(\)\s*\.clamp\(0\.0, maxVal\),)"
    replacement_slider = r"secondaryTrackValue: _buffer.inMilliseconds.toDouble().clamp(0.0, maxVal),\n                                                    \1"
    content = re.sub(pattern_slider, replacement_slider, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

add_buffer_ui('lib/screens/player_screen.dart')
print("Patched Buffer UI")
