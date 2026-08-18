import io

with io.open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    settings = f.read()

settings = settings.replace('GlobalColorSettings(prefs: _prefs!),', 'GlobalColorSettings(prefs: _prefs!, onSettingsChanged: (_) {}),')

with io.open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(settings)

print('Fixed build errors!')
