import os
content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

import_settings = "import 'settings_screen.dart';\\n"
if "import 'settings_screen.dart';" not in content:
    content = content.replace("import '../utils/l10n.dart';", import_settings + "import '../utils/l10n.dart';")

old_push = '''              Navigator.pushNamed(context, '/settings').then((_) {
                _loadSettings();
              });'''

new_push = '''              Navigator.push(context, MaterialPageRoute(builder: (_) => const SettingsScreen())).then((_) {
                _loadSettings();
              });'''

content = content.replace(old_push, new_push)

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
