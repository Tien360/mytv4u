import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add _prefs variable
content = content.replace('Map<String, dynamic>? _appSettings;', 'SharedPreferences? _prefs;\n  Map<String, dynamic>? _appSettings;')

# 2. Add Firebase sync method and modify _loadSettings to sync from Firebase
new_load_settings = '''  Future<void> _loadSettings() async {
    _prefs = await SharedPreferences.getInstance();
    
    // Sync from Firebase
    final fbSettings = await FirebaseApi.loadUserSettings();
    if (fbSettings != null) {
      if (fbSettings.containsKey('enabled_sources')) {
        final sourcesList = fbSettings['enabled_sources'] as List<String>;
        await _prefs!.setStringList('enabled_sources', sourcesList);
      }
      if (fbSettings.containsKey('enable_hw_accel')) await _prefs!.setBool('enable_hw_accel', fbSettings['enable_hw_accel']);
      if (fbSettings.containsKey('sub_size')) await _prefs!.setDouble('sub_size', fbSettings['sub_size']);
      if (fbSettings.containsKey('sub_opacity')) await _prefs!.setDouble('sub_opacity', fbSettings['sub_opacity']);
      if (fbSettings.containsKey('sub_color')) await _prefs!.setString('sub_color', fbSettings['sub_color']);
      if (fbSettings.containsKey('sub_font')) await _prefs!.setString('sub_font', fbSettings['sub_font']);
      if (fbSettings.containsKey('auto_next')) await _prefs!.setBool('auto_next', fbSettings['auto_next']);
      if (fbSettings.containsKey('auto_play_trailer')) await _prefs!.setBool('auto_play_trailer', fbSettings['auto_play_trailer']);
      if (fbSettings.containsKey('default_speed')) await _prefs!.setDouble('default_speed', fbSettings['default_speed']);
      if (fbSettings.containsKey('watch_limit')) await _prefs!.setInt('watch_limit', fbSettings['watch_limit']);
      if (fbSettings.containsKey('app_lang')) await _prefs!.setString('app_lang', fbSettings['app_lang']);
      if (fbSettings.containsKey('background_playback')) await _prefs!.setBool('background_playback', fbSettings['background_playback']);
      if (fbSettings.containsKey('color_preset')) await _prefs!.setString('color_preset', fbSettings['color_preset']);
      if (fbSettings.containsKey('color_brightness')) await _prefs!.setDouble('color_brightness', fbSettings['color_brightness']);
      if (fbSettings.containsKey('color_contrast')) await _prefs!.setDouble('color_contrast', fbSettings['color_contrast']);
      if (fbSettings.containsKey('color_saturation')) await _prefs!.setDouble('color_saturation', fbSettings['color_saturation']);
    }

    final prefs = _prefs!;'''
content = content.replace('''  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();''', new_load_settings)

# 3. Method to trigger sync to Firebase
sync_method = '''  void _syncToFirebase() {
    if (_prefs == null) return;
    final keys = [
      'enabled_sources', 'enable_hw_accel', 'sub_size', 'sub_opacity', 'sub_color', 'sub_font',
      'auto_next', 'auto_play_trailer', 'default_speed', 'watch_limit', 'app_lang', 'background_playback',
      'color_preset', 'color_brightness', 'color_contrast', 'color_saturation'
    ];
    final Map<String, dynamic> data = {};
    for (final key in keys) {
      final val = _prefs!.get(key);
      if (val != null) data[key] = val;
    }
    FirebaseApi.saveUserSettings(data);
  }'''
content = content.replace('Future<void> _saveSources() async {', sync_method + '\n\n  Future<void> _saveSources() async {')

# 4. Modify all setState inside SettingsScreen to call _syncToFirebase()
# E.g. _saveSources() -> _saveSources().then((_) => _syncToFirebase());
# It's better to just add _syncToFirebase() inside _saveSources()
content = content.replace('''    await prefs.setStringList('enabled_sources', enabledList);
  }''', '''    await prefs.setStringList('enabled_sources', enabledList);
    _syncToFirebase();
  }''')

# For other individual toggles, we can just replace wait prefs.set... with wait prefs.set...; _syncToFirebase();
content = content.replace('''await prefs.setBool('enable_hw_accel', val);''', '''await prefs.setBool('enable_hw_accel', val); _syncToFirebase();''')
content = content.replace('''await prefs.setBool('auto_next', val);''', '''await prefs.setBool('auto_next', val); _syncToFirebase();''')
content = content.replace('''await prefs.setBool('auto_play_trailer', val);''', '''await prefs.setBool('auto_play_trailer', val); _syncToFirebase();''')
content = content.replace('''await prefs.setBool('background_playback', val);''', '''await prefs.setBool('background_playback', val); _syncToFirebase();''')
content = content.replace('''await prefs.setDouble('sub_size', val);''', '''await prefs.setDouble('sub_size', val); _syncToFirebase();''')
content = content.replace('''await prefs.setDouble('sub_opacity', val);''', '''await prefs.setDouble('sub_opacity', val); _syncToFirebase();''')
content = content.replace('''await prefs.setString('sub_color', val);''', '''await prefs.setString('sub_color', val); _syncToFirebase();''')
content = content.replace('''await prefs.setString('sub_font', val);''', '''await prefs.setString('sub_font', val); _syncToFirebase();''')
content = content.replace('''await prefs.setDouble('default_speed', val);''', '''await prefs.setDouble('default_speed', val); _syncToFirebase();''')
content = content.replace('''await prefs.setInt('watch_limit', limit);''', '''await prefs.setInt('watch_limit', limit); _syncToFirebase();''')
content = content.replace('''await prefs.setString('app_lang', val);''', '''await prefs.setString('app_lang', val); _syncToFirebase();''')

# 5. Inject GlobalColorSettings widget before Nguon Phim
inject_ui = '''
                          const SizedBox(height: 32),
                          _buildSectionTitle(Icons.color_lens, 'Màu sắc Video (Toàn cục)'),
                          const SizedBox(height: 16),
                          if (_prefs != null)
                            GlassContainer(
                              padding: const EdgeInsets.all(16),
                              borderRadius: 16,
                              color: Colors.white.withOpacity(0.05),
                              borderColor: Colors.white.withOpacity(0.1),
                              child: GlobalColorSettings(
                                prefs: _prefs!,
                                onSettingsChanged: (data) => _syncToFirebase(),
                              ),
                            ),
                          const SizedBox(height: 32),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              _buildSectionTitle(Icons.source, L10n.t('movie_sources')),'''
content = content.replace('''                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                _buildSectionTitle(Icons.source, L10n.t('movie_sources')),''', inject_ui)

# 6. Add import for global_color_settings
content = content.replace("import '../widgets/glass_container.dart';", "import '../widgets/glass_container.dart';\nimport '../widgets/global_color_settings.dart';")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched settings_screen.dart UI and Firebase sync')
