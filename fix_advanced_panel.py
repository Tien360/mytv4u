import re
content = open('lib/widgets/advanced_controls_panel.dart', 'r', encoding='utf-8').read()

old_load = '''  void _loadProperties() {
    // MediaKit MPV doesn't easily expose getters for these dynamically without async.
    // In a real app we'd track these in the parent. For now, default to 0.
  }'''

new_load = '''  void _loadProperties() async {
    final prefs = await SharedPreferences.getInstance();
    if (mounted) {
      setState(() {
        _preset = prefs.getString('color_preset') ?? 'default';
        _brightness = prefs.getDouble('color_brightness') ?? 0.0;
        _contrast = prefs.getDouble('color_contrast') ?? 0.0;
        _saturation = prefs.getDouble('color_saturation') ?? 0.0;
      });
    }
  }
  
  void _saveProperties() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('color_preset', _preset);
    await prefs.setDouble('color_brightness', _brightness);
    await prefs.setDouble('color_contrast', _contrast);
    await prefs.setDouble('color_saturation', _saturation);
  }'''
content = content.replace(old_load, new_load)

if 'shared_preferences.dart' not in content:
    content = content.replace("import 'glass_container.dart';", "import 'glass_container.dart';\nimport 'package:shared_preferences/shared_preferences.dart';")

old_preset = '''  void _onPresetSelected(String presetName) {
    if (presetName == 'custom') return;
    setState(() {
      _preset = presetName;
      _brightness = _presets[presetName]!['brightness']!;
      _contrast = _presets[presetName]!['contrast']!;
      _saturation = _presets[presetName]!['saturation']!;
      _applyPropertiesToPlayer();
    });
  }'''

new_preset = '''  void _onPresetSelected(String presetName) {
    if (presetName == 'custom') return;
    setState(() {
      _preset = presetName;
      _brightness = _presets[presetName]!['brightness']!;
      _contrast = _presets[presetName]!['contrast']!;
      _saturation = _presets[presetName]!['saturation']!;
      _applyPropertiesToPlayer();
    });
    _saveProperties();
  }'''
content = content.replace(old_preset, new_preset)

old_slider = '''  void _onSliderChanged(String type, double val) {
    setState(() {
      if (type == 'brightness') { _brightness = val; _preset = 'custom'; }
      if (type == 'contrast') { _contrast = val; _preset = 'custom'; }
      if (type == 'saturation') { _saturation = val; _preset = 'custom'; }
      _applyPropertiesToPlayer();
    });
  }'''

new_slider = '''  void _onSliderChanged(String type, double val) {
    setState(() {
      if (type == 'brightness') { _brightness = val; _preset = 'custom'; }
      if (type == 'contrast') { _contrast = val; _preset = 'custom'; }
      if (type == 'saturation') { _saturation = val; _preset = 'custom'; }
      _applyPropertiesToPlayer();
    });
  }

  void _onSliderChangeEnd() {
    _saveProperties();
  }'''
content = content.replace(old_slider, new_slider)

content = re.sub(r'(Slider\(\s*.*?onChanged:\s*\(val\)\s*=>\s*_onSliderChanged\([^,]+,\s*val\)\s*,)', r'\1 onChangeEnd: (val) => _onSliderChangeEnd(),', content, flags=re.DOTALL)

open('lib/widgets/advanced_controls_panel.dart', 'w', encoding='utf-8').write(content)
