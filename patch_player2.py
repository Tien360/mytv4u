import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Imports
if 'advanced_controls_panel.dart' not in content:
    content = content.replace("import '../widgets/glass_container.dart';", "import '../widgets/glass_container.dart';\nimport '../widgets/advanced_controls_panel.dart';\nimport 'package:shared_preferences/shared_preferences.dart';")

# 2. Add state variable
if 'SidePanelMode _activePanel' not in content:
    content = content.replace('bool _isLocked = false;', 'bool _isLocked = false;\n  SidePanelMode _activePanel = SidePanelMode.none;')

# 3. Add _applyGlobalColorSettings
if '_applyGlobalColorSettings' not in content:
    func = '''
  Future<void> _applyGlobalColorSettings() async {
    final prefs = await SharedPreferences.getInstance();
    final brightness = prefs.getDouble('color_brightness') ?? 0.0;
    final contrast = prefs.getDouble('color_contrast') ?? 0.0;
    final saturation = prefs.getDouble('color_saturation') ?? 0.0;

    try {
      (_player.platform as dynamic).setProperty('brightness', brightness.toString());
      (_player.platform as dynamic).setProperty('contrast', contrast.toString());
      (_player.platform as dynamic).setProperty('saturation', saturation.toString());
    } catch (e) {
      print('Cannot apply color properties to player: \');
    }
  }
'''
    content = content.replace('Future<void> _initEpisode() async {', func + '\n  Future<void> _initEpisode() async {')
    content = content.replace("await _player.open(Media(episode.m3u8Url!));", "await _player.open(Media(episode.m3u8Url!));\n      await _applyGlobalColorSettings();")

# 4. Add to Stack
if 'SideControlPanel' not in content:
    stack_end = '''              if (_activePanel != SidePanelMode.none)
                Positioned.fill(
                  child: Row(
                    children: [
                      Expanded(
                        child: GestureDetector(
                          onTap: () => setState(() => _activePanel = SidePanelMode.none),
                          child: Container(color: Colors.transparent),
                        ),
                      ),
                      SideControlPanel(
                        player: _player,
                        mode: _activePanel,
                        onClose: () => setState(() => _activePanel = SidePanelMode.none),
                      ),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
    );'''
    content = content.replace('''            ],
          ),
        ),
      ),
    );
  }

  void _showSettingsDialog() {''', stack_end + '\n  }\n\n  void _showSettingsDialog() {')

# 5. Add Buttons in Tabs
btn_color = '''                                ListTile(
                                  leading: const Icon(Icons.color_lens, color: Colors.blueAccent),
                                  title: const Text('Bá»™ lá» c mÃ u Video', style: TextStyle(color: Colors.white)),
                                  trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                                  onTap: () {
                                    Navigator.pop(context);
                                    setState(() => _activePanel = SidePanelMode.color);
                                  },
                                ),
                                const Divider(color: Colors.white24),'''
# Insert into Chung Tab before playback speed
content = content.replace('''                          // Tab Chung
                          StatefulBuilder(
                            builder: (context, setTabState) => ListView(
                              padding: const EdgeInsets.all(16),
                              children: [''', '''                          // Tab Chung
                          StatefulBuilder(
                            builder: (context, setTabState) => ListView(
                              padding: const EdgeInsets.all(16),
                              children: [
''' + btn_color)

btn_audio = '''                                ListTile(
                                  leading: const Icon(Icons.av_timer, color: Colors.blueAccent),
                                  title: const Text('Ä á»“ng bá»™ trÃª áº¢m thanh', style: TextStyle(color: Colors.white)),
                                  trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                                  onTap: () {
                                    Navigator.pop(context);
                                    setState(() => _activePanel = SidePanelMode.audio);
                                  },
                                ),
                                const Divider(color: Colors.white24),'''
# Insert into Audio Tab
content = content.replace('''                          // Tab Ã‚m thanh
                          StatefulBuilder(
                            builder: (context, setTabState) => ListView(
                              padding: const EdgeInsets.all(16),
                              children: [''', '''                          // Tab Ã‚m thanh
                          StatefulBuilder(
                            builder: (context, setTabState) => ListView(
                              padding: const EdgeInsets.all(16),
                              children: [
''' + btn_audio)

btn_sub = '''                                ListTile(
                                  leading: const Icon(Icons.av_timer, color: Colors.blueAccent),
                                  title: const Text('Ä á»“ng bá»™ trÃª Phá»¥ Ä‘á» ', style: TextStyle(color: Colors.white)),
                                  trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                                  onTap: () {
                                    Navigator.pop(context);
                                    setState(() => _activePanel = SidePanelMode.subtitle);
                                  },
                                ),
                                const Divider(color: Colors.white24),'''
# Insert into Main Sub Tab
content = content.replace('''                          // Tab Phá»¥ Ä‘á»  ChÃ­nh
                          StatefulBuilder(
                            builder: (context, setTabState) => ListView(
                              padding: const EdgeInsets.all(16),
                              children: [''', '''                          // Tab Phá»¥ Ä‘á»  ChÃ­nh
                          StatefulBuilder(
                            builder: (context, setTabState) => ListView(
                              padding: const EdgeInsets.all(16),
                              children: [
''' + btn_sub)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched player_screen.dart correctly')
