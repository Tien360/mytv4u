import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';
import 'package:shared_preferences/shared_preferences.dart';

class GlobalColorSettings extends StatefulWidget {
  final SharedPreferences prefs;
  final Function(Map<String, dynamic>) onSettingsChanged;

  const GlobalColorSettings({
    super.key,
    required this.prefs,
    required this.onSettingsChanged,
  });

  @override
  State<GlobalColorSettings> createState() => _GlobalColorSettingsState();
}

class _GlobalColorSettingsState extends State<GlobalColorSettings> {
  late final Player _previewPlayer;
  late final VideoController _previewController;
  bool _isPlayerInitialized = false;

  String _preset = 'Mặc định';
  double _brightness = 0.0;
  double _contrast = 0.0;
  double _saturation = 0.0;

  final Map<String, Map<String, double>> _presets = {
    'Mặc định': {'brightness': 0.0, 'contrast': 0.0, 'saturation': 0.0},
    'Sống động': {'brightness': 5.0, 'contrast': 10.0, 'saturation': 25.0},
    'Rạp phim': {'brightness': -5.0, 'contrast': 15.0, 'saturation': 5.0},
    'Sáng rực': {'brightness': 20.0, 'contrast': 5.0, 'saturation': 0.0},
    'Đen trắng': {'brightness': 0.0, 'contrast': 5.0, 'saturation': -100.0},
    'Ấm áp': {'brightness': 0.0, 'contrast': 5.0, 'saturation': 15.0},
    'Lạnh': {'brightness': 5.0, 'contrast': 5.0, 'saturation': -10.0},
    'Tùy chỉnh': {},
  };

  @override
  void initState() {
    super.initState();
    _loadSettings();
    _initPlayer();
  }

  void _loadSettings() {
    _preset = widget.prefs.getString('color_preset') ?? 'Mặc định';
    _brightness = widget.prefs.getDouble('color_brightness') ?? 0.0;
    _contrast = widget.prefs.getDouble('color_contrast') ?? 0.0;
    _saturation = widget.prefs.getDouble('color_saturation') ?? 0.0;
  }

  Future<void> _initPlayer() async {
    _previewPlayer = Player();
    _previewController = VideoController(_previewPlayer);
    await _previewPlayer.open(Media('https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8'));
    await _previewPlayer.setPlaylistMode(PlaylistMode.loop);
    await _previewPlayer.setVolume(0);
    setState(() => _isPlayerInitialized = true);
    
    // Apply initial settings
    _applyPropertiesToPlayer();
  }

  void _applyPropertiesToPlayer() {
    try {
      (_previewPlayer.platform as dynamic).setProperty('brightness', _brightness.toString());
      (_previewPlayer.platform as dynamic).setProperty('contrast', _contrast.toString());
      (_previewPlayer.platform as dynamic).setProperty('saturation', _saturation.toString());
    } catch (e) {}
  }

  @override
  void dispose() {
    _previewPlayer.dispose();
    super.dispose();
  }

  void _saveSettings() {
    widget.prefs.setString('color_preset', _preset);
    widget.prefs.setDouble('color_brightness', _brightness);
    widget.prefs.setDouble('color_contrast', _contrast);
    widget.prefs.setDouble('color_saturation', _saturation);
    widget.onSettingsChanged({
      'color_preset': _preset,
      'color_brightness': _brightness,
      'color_contrast': _contrast,
      'color_saturation': _saturation,
    });
  }

  void _onPresetSelected(String presetName) {
    if (presetName == 'Tùy chỉnh') return;
    setState(() {
      _preset = presetName;
      _brightness = _presets[presetName]!['brightness']!;
      _contrast = _presets[presetName]!['contrast']!;
      _saturation = _presets[presetName]!['saturation']!;
      _applyPropertiesToPlayer();
    });
    _saveSettings();
  }

  void _onSliderChanged(String type, double val) {
    setState(() {
      _preset = 'Tùy chỉnh';
      if (type == 'brightness') _brightness = val;
      if (type == 'contrast') _contrast = val;
      if (type == 'saturation') _saturation = val;
      _applyPropertiesToPlayer();
    });
  }
  
  void _onSliderChangeEnd() {
    _saveSettings();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Video chạy mẫu:', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Container(
          height: 180,
          width: double.infinity,
          decoration: BoxDecoration(
            color: Colors.black,
            borderRadius: BorderRadius.circular(12),
          ),
          clipBehavior: Clip.hardEdge,
          child: _isPlayerInitialized 
              ? Video(controller: _previewController, fit: BoxFit.cover)
              : const Center(child: CircularProgressIndicator()),
        ),
        const SizedBox(height: 16),
        const Text('Bộ lọc có sẵn:', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: _presets.keys.map((p) {
            final isSelected = p == _preset;
            return ChoiceChip(
              label: Text(p),
              selected: isSelected,
              selectedColor: Colors.blueAccent,
              backgroundColor: Colors.white10,
              labelStyle: TextStyle(color: isSelected ? Colors.white : Colors.white70),
              onSelected: (val) => _onPresetSelected(p),
            );
          }).toList(),
        ),
        const SizedBox(height: 16),
        _buildSlider('Độ sáng', _brightness, -100, 100, (v) => _onSliderChanged('brightness', v)),
        _buildSlider('Tương phản', _contrast, -100, 100, (v) => _onSliderChanged('contrast', v)),
        _buildSlider('Độ bão hòa màu', _saturation, -100, 100, (v) => _onSliderChanged('saturation', v)),
      ],
    );
  }

  Widget _buildSlider(String label, double value, double min, double max, Function(double) onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: const TextStyle(color: Colors.white70, fontSize: 13)),
            Text('', style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold)),
          ],
        ),
        Slider(
          value: value,
          min: min,
          max: max,
          divisions: (max - min).toInt(),
          activeColor: Colors.blueAccent,
          inactiveColor: Colors.white24,
          onChanged: onChanged,
          onChangeEnd: (_) => _onSliderChangeEnd(),
        ),
      ],
    );
  }
}
