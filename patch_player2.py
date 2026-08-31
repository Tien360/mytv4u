import re

content = open('lib/screens/player_screen.dart', 'r', encoding='utf-8').read()

if "prefs.getBool('auto_next')" not in content:
    content = content.replace(
        "_subOpacity = prefs.getDouble('sub_opacity') ?? 0.3;",
        "_subOpacity = prefs.getDouble('sub_opacity') ?? 0.3;\n          _autoNext = prefs.getBool('auto_next') ?? true;\n          _playbackSpeed = prefs.getDouble('default_speed') ?? 1.0;\n          _backgroundPlayback = prefs.getBool('background_playback') ?? false;"
    )

if 'bool _backgroundPlayback = false;' not in content:
    content = content.replace("bool _autoNext = true;", "bool _autoNext = true;\n  bool _backgroundPlayback = false;")

open('lib/screens/player_screen.dart', 'w', encoding='utf-8').write(content)
print("Patched player_screen.dart prefs loading!")
