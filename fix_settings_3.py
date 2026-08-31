content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
content = content.replace('bool _backgroundPlayback = false;', '''bool _backgroundPlayback = false;

  String _visualizerType = 'bars';
  bool _showVinyl = true;
  int _sleepTimerMinutes = 0;''')

old_load = '''      _backgroundPlayback = prefs.getBool('background_playback') ?? false;'''
new_load = '''      _backgroundPlayback = prefs.getBool('background_playback') ?? false;
      _visualizerType = prefs.getString('audio_visualizer') ?? 'bars';
      _showVinyl = prefs.getBool('audio_vinyl') ?? true;
      _sleepTimerMinutes = prefs.getInt('audio_sleep_timer') ?? 0;'''
content = content.replace(old_load, new_load)

# Add to _loadSettingsFromFirebase
old_fb_load = '''      if (fbSettings.containsKey('background_playback'))
        await _prefs!.setBool(
          'background_playback',
          fbSettings['background_playback'],
        );'''
new_fb_load = '''      if (fbSettings.containsKey('background_playback'))
        await _prefs!.setBool(
          'background_playback',
          fbSettings['background_playback'],
        );
      if (fbSettings.containsKey('audio_visualizer')) await _prefs!.setString('audio_visualizer', fbSettings['audio_visualizer']);
      if (fbSettings.containsKey('audio_vinyl')) await _prefs!.setBool('audio_vinyl', fbSettings['audio_vinyl']);
      if (fbSettings.containsKey('audio_sleep_timer')) await _prefs!.setInt('audio_sleep_timer', fbSettings['audio_sleep_timer']);'''
content = content.replace(old_fb_load, new_fb_load)

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
