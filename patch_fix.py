import io
import re

# 1. Fix player_screen.dart
with io.open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    player = f.read()

player = player.replace('bool _isExternalPlayerActive = false;', 'bool _isExternalPlayerActive = false;\n  SidePanelMode _activePanel = SidePanelMode.none;')

with io.open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(player)

# 2. Fix settings_screen.dart
with io.open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    settings = f.read()

settings = settings.replace('const GlobalColorSettings(),', 'if (_prefs != null) GlobalColorSettings(prefs: _prefs!),')

with io.open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(settings)

print('Fixed build errors!')
