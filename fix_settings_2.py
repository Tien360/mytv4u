import re
content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
content = re.sub(r'GlobalColorSettings\(\s*prefs:\s*_prefs!,\s*onSettingsChanged:\s*\(_\)\s*\{\},\s*\)',
r'''GlobalColorSettings(
  prefs: _prefs!,
  onSettingsChanged: (_) {
    _syncToFirebase();
  },
)''', content)
open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
