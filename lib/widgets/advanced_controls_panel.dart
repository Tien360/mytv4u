import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:mytv4u_flutter/widgets/glass_container.dart';

class AdvancedControlsTab extends StatefulWidget {
  final Player player;
  

  const AdvancedControlsTab({
    Key? key,
    required this.player,
    
  }) : super(key: key);

  @override
  State<AdvancedControlsTab> createState() => _AdvancedControlsTabState();
}

class _AdvancedControlsTabState extends State<AdvancedControlsTab> {
  double _brightness = 0;
  double _contrast = 0;
  double _saturation = 0;
  double _audioDelay = 0;
  double _subDelay = 0;

  // Cấu hình các bộ lọc mẫu
  final Map<String, Map<String, double>> _presets = {
    'Mặc định': {'brightness': 0, 'contrast': 0, 'saturation': 0},
    'Sống động': {'brightness': 5, 'contrast': 10, 'saturation': 20},
    'Rạp phim': {'brightness': -5, 'contrast': 15, 'saturation': -5},
    'Sáng rực': {'brightness': 15, 'contrast': 5, 'saturation': 10},
    'Đen trắng': {'brightness': 0, 'contrast': 0, 'saturation': -100},
  };
  String _selectedPreset = 'Mặc định';

  Future<void> _setMpvProperty(String name, String value) async {
    try {
      final dynamic platform = widget.player.platform;
      await platform.setProperty(name, value);
    } catch (e) {
      print('Lỗi setProperty $name: $e');
    }
  }

  void _applyPreset(String name) {
    if (!_presets.containsKey(name)) return;
    final preset = _presets[name]!;
    
    setState(() {
      _selectedPreset = name;
      _brightness = preset['brightness']!;
      _contrast = preset['contrast']!;
      _saturation = preset['saturation']!;
    });

    _setMpvProperty('brightness', _brightness.toInt().toString());
    _setMpvProperty('contrast', _contrast.toInt().toString());
    _setMpvProperty('saturation', _saturation.toInt().toString());
  }

  void _resetDelay() {
    setState(() {
      _audioDelay = 0;
      _subDelay = 0;
    });
    _setMpvProperty('audio-delay', '0');
    _setMpvProperty('sub-delay', '0');
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
const Text('Màu sắc Video', style: TextStyle(color: Colors.blueAccent, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 12),
                  
                  // Presets
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: _presets.keys.map((name) {
                        final isSelected = _selectedPreset == name;
                        return Padding(
                          padding: const EdgeInsets.only(right: 8),
                          child: ChoiceChip(
                            label: Text(name, style: TextStyle(color: isSelected ? Colors.white : Colors.white70)),
                            selected: isSelected,
                            selectedColor: Colors.blueAccent,
                            backgroundColor: Colors.white10,
                            onSelected: (val) => _applyPreset(name),
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                  const SizedBox(height: 16),
                  
                  // Sliders
                  _buildSlider('Độ sáng', _brightness, -100, 100, (val) {
                    setState(() {
                      _brightness = val;
                      _selectedPreset = 'Tùy chỉnh';
                    });
                    _setMpvProperty('brightness', val.toInt().toString());
                  }),
                  _buildSlider('Tương phản', _contrast, -100, 100, (val) {
                    setState(() {
                      _contrast = val;
                      _selectedPreset = 'Tùy chỉnh';
                    });
                    _setMpvProperty('contrast', val.toInt().toString());
                  }),
                  _buildSlider('Bão hòa', _saturation, -100, 100, (val) {
                    setState(() {
                      _saturation = val;
                      _selectedPreset = 'Tùy chỉnh';
                    });
                    _setMpvProperty('saturation', val.toInt().toString());
                  }),
                  
                  const Divider(color: Colors.white24, height: 32),
                  
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Đồng bộ (Audio/Sub)', style: TextStyle(color: Colors.orangeAccent, fontWeight: FontWeight.bold)),
                      TextButton(onPressed: _resetDelay, child: const Text('Reset', style: TextStyle(color: Colors.white54))),
                    ],
                  ),
                  const SizedBox(height: 8),
                  
                  _buildSlider('Trễ Âm thanh', _audioDelay, -5, 5, (val) {
                    setState(() => _audioDelay = val);
                    _setMpvProperty('audio-delay', val.toStringAsFixed(2));
                  }, isFloat: true),
                  
                  _buildSlider('Trễ Phụ đề', _subDelay, -5, 5, (val) {
                    setState(() => _subDelay = val);
                    _setMpvProperty('sub-delay', val.toStringAsFixed(2));
                  }, isFloat: true),
                ],
              ),
    );
  }

  Widget _buildSlider(String label, double value, double min, double max, Function(double) onChanged, {bool isFloat = false}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: const TextStyle(color: Colors.white70, fontSize: 13)),
            Text(isFloat ? '${value > 0 ? '+' : ''}${value.toStringAsFixed(1)}s' : '${value > 0 ? '+' : ''}${value.toInt()}', style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold)),
          ],
        ),
        Slider(
          value: value,
          min: min,
          max: max,
          divisions: isFloat ? ((max - min) * 10).toInt() : (max - min).toInt(),
          activeColor: isFloat ? Colors.orangeAccent : Colors.blueAccent,
          inactiveColor: Colors.white24,
          onChanged: onChanged,
        ),
      ],
    );
  }
}
