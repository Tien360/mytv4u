content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

# 1. Fix GlobalColorSettings onSettingsChanged
content = content.replace(
'''                                    if (_prefs != null)
                                      GlobalColorSettings(
                                        prefs: _prefs!,
                                        onSettingsChanged: (_) {},
                                      ),''',
'''                                    if (_prefs != null)
                                      GlobalColorSettings(
                                        prefs: _prefs!,
                                        onSettingsChanged: (_) {
                                          _syncToFirebase();
                                        },
                                      ),'''
)

# 2. Add Audio settings keys to _syncToFirebase
old_sync_keys = '''      'color_brightness',
      'color_contrast',
      'color_saturation',
    ];'''
new_sync_keys = '''      'color_brightness',
      'color_contrast',
      'color_saturation',
      'audio_visualizer',
      'audio_vinyl',
      'audio_sleep_timer',
    ];'''
content = content.replace(old_sync_keys, new_sync_keys)

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
