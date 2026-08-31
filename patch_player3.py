import re

content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()

if 'bool _enableSkipIntro = true;' not in content:
    content = content.replace("bool _backgroundPlayback = false;", "bool _backgroundPlayback = false;\n  bool _enableSkipIntro = true;\n  int _skipIntroDuration = 85;")
    content = content.replace("_backgroundPlayback = prefs.getBool('background_playback') ?? false;", "_backgroundPlayback = prefs.getBool('background_playback') ?? false;\n          _enableSkipIntro = prefs.getBool('enable_skip_intro') ?? true;\n          _skipIntroDuration = prefs.getInt('skip_intro_duration') ?? 85;")

content = re.sub(r"if \(\!widget\.isLive &&\s*_duration\.inSeconds > 85 &&\s*_position\.inSeconds > 0 &&\s*_position\.inSeconds < 85 &&\s*\!_isUsingWebview\)", "if (!widget.isLive && _enableSkipIntro && _duration.inSeconds > _skipIntroDuration && _position.inSeconds > 0 && _position.inSeconds < _skipIntroDuration && !_isUsingWebview)", content)

content = content.replace("player.seek(const Duration(seconds: 85));", "player.seek(Duration(seconds: _skipIntroDuration));")

open('lib/screens/player_screen.dart', 'w', encoding='utf-8').write(content)
print("Patched skip intro player!")
