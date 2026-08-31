import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

# 1. State vars
content = content.replace('bool _showPlaylist = false;', 'bool _showPlaylist = false;\n  bool showVinyl = true;')

# 2. _spinController duration
content = content.replace('duration: const Duration(seconds: 3)', 'duration: const Duration(seconds: 10)')

# 3. _loadSettings
old_settings = '''  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      visualizerType = prefs.getString('audio_visualizer') ?? 'bars';
      sleepTimerMinutes = prefs.getInt('audio_sleep_timer') ?? 0;
    });'''
new_settings = '''  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      visualizerType = prefs.getString('audio_visualizer') ?? 'bars';
      sleepTimerMinutes = prefs.getInt('audio_sleep_timer') ?? 0;
      showVinyl = prefs.getBool('audio_vinyl') ?? true;
    });'''
content = content.replace(old_settings, new_settings)

open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
