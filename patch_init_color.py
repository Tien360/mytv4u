import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

apply_method = '''
  Future<void> _applyGlobalColorSettings() async {
    final prefs = await SharedPreferences.getInstance();
    final brightness = prefs.getDouble('color_brightness') ?? 0.0;
    final contrast = prefs.getDouble('color_contrast') ?? 0.0;
    final saturation = prefs.getDouble('color_saturation') ?? 0.0;
    
    try {
      (player.platform as dynamic).setProperty('brightness', brightness.toString());
      (player.platform as dynamic).setProperty('contrast', contrast.toString());
      (player.platform as dynamic).setProperty('saturation', saturation.toString());
    } catch (e) {}
  }
'''

# Find _initEpisode
# await player.open(Media(m3u8), play: false); ...
content = content.replace("await player.open(Media(m3u8), play: false);", "await player.open(Media(m3u8), play: false);\n      _applyGlobalColorSettings();")
content = content.replace("await player.open(Media(url!), play: false);", "await player.open(Media(url!), play: false);\n        _applyGlobalColorSettings();")

# Inject method
content = content.replace("  Future<void> _initEpisode() async {", apply_method + "\n  Future<void> _initEpisode() async {")

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched apply global color')
