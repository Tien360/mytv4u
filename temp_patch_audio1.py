with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Variables
vars_search = "bool _backgroundPlayback = false;"
vars_replace = """bool _backgroundPlayback = false;
  String _audioVisualizer = 'bars';
  int _audioSleepTimer = 0;
  bool _audioVinyl = true;"""

idx = content.find(vars_search)
if idx != -1:
    content = content[:idx] + vars_replace + content[idx+len(vars_search):]
    print("Injected state variables")

# Global keys
keys_search = "final GlobalKey _systemKey = GlobalKey();"
keys_replace = """final GlobalKey _systemKey = GlobalKey();
  final GlobalKey _audioKey = GlobalKey();"""
idx2 = content.find(keys_search)
if idx2 != -1:
    content = content[:idx2] + keys_replace + content[idx2+len(keys_search):]
    print("Injected GlobalKey")

# Firebase Sync Keys
keys_fb_search = """      'color_brightness',
      'color_contrast',
      'color_saturation',
    ];"""
keys_fb_replace = """      'color_brightness',
      'color_contrast',
      'color_saturation',
      'audio_visualizer',
      'audio_sleep_timer',
      'audio_vinyl',
    ];"""
idx3 = content.find(keys_fb_search)
if idx3 != -1:
    content = content[:idx3] + keys_fb_replace + content[idx3+len(keys_fb_search):]
    print("Injected keys to _syncToFirebase")

# Load Settings
load_fb_search = """      if (fbSettings.containsKey('background_playback'))
        await _prefs!.setBool(
          'background_playback',
          fbSettings['background_playback'],
        );"""
load_fb_replace = load_fb_search + """
      if (fbSettings.containsKey('audio_visualizer'))
        await _prefs!.setString('audio_visualizer', fbSettings['audio_visualizer']);
      if (fbSettings.containsKey('audio_sleep_timer'))
        await _prefs!.setInt('audio_sleep_timer', fbSettings['audio_sleep_timer']);
      if (fbSettings.containsKey('audio_vinyl'))
        await _prefs!.setBool('audio_vinyl', fbSettings['audio_vinyl']);"""
idx4 = content.find(load_fb_search)
if idx4 != -1:
    content = content[:idx4] + load_fb_replace + content[idx4+len(load_fb_search):]
    print("Injected Firebase load settings")

# Load SharedPreferences local
load_sp_search = "_backgroundPlayback = prefs.getBool('background_playback') ?? false;"
load_sp_replace = """_backgroundPlayback = prefs.getBool('background_playback') ?? false;
        _audioVisualizer = prefs.getString('audio_visualizer') ?? 'bars';
        _audioSleepTimer = prefs.getInt('audio_sleep_timer') ?? 0;
        _audioVinyl = prefs.getBool('audio_vinyl') ?? true;"""
idx5 = content.find(load_sp_search)
if idx5 != -1:
    content = content[:idx5] + load_sp_replace + content[idx5+len(load_sp_search):]
    print("Injected SharedPreferences load")

# Logout clear
logout_search = "await prefs.remove('background_playback');"
logout_replace = """await prefs.remove('background_playback');
                await prefs.remove('audio_visualizer');
                await prefs.remove('audio_sleep_timer');
                await prefs.remove('audio_vinyl');"""
idx6 = content.find(logout_search)
if idx6 != -1:
    content = content[:idx6] + logout_replace + content[idx6+len(logout_search):]
    print("Injected Logout clear")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
