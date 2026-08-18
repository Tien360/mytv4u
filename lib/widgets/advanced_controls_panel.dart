import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'glass_container.dart';

enum SidePanelMode { none, color, subtitle, audio }

class SideControlPanel extends StatefulWidget {
  final Player player;
  final SidePanelMode mode;
  final VoidCallback onClose;

  const SideControlPanel({
    super.key,
    required this.player,
    required this.mode,
    required this.onClose,
  });

  @override
  State<SideControlPanel> createState() => _SideControlPanelState();
}

class _SideControlPanelState extends State<SideControlPanel> {
  String _preset = 'Mặc định';
  double _brightness = 0.0;
  double _contrast = 0.0;
  double _saturation = 0.0;
  
  double _subDelay = 0.0;
  double _audioDelay = 0.0;

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
    _loadProperties();
  }

  void _loadProperties() {
    // MediaKit MPV doesn't easily expose getters for these dynamically without async.
    // In a real app we'd track these in the parent. For now, default to 0.
  }

  void _applyPropertiesToPlayer() {
    try {
      (widget.player.platform as dynamic).setProperty('brightness', _brightness.toString());
      (widget.player.platform as dynamic).setProperty('contrast', _contrast.toString());
      (widget.player.platform as dynamic).setProperty('saturation', _saturation.toString());
    } catch (e) {}
  }
  
  void _applyDelay(String type, double val) {
    try {
      (widget.player.platform as dynamic).setProperty(type, (val / 1000.0).toString());
    } catch (e) {}
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
  }

  void _onSliderChanged(String type, double val) {
    setState(() {
      if (type == 'brightness') { _brightness = val; _preset = 'Tùy chỉnh'; }
      if (type == 'contrast') { _contrast = val; _preset = 'Tùy chỉnh'; }
      if (type == 'saturation') { _saturation = val; _preset = 'Tùy chỉnh'; }
      if (type == 'sub-delay') { _subDelay = val; _applyDelay(type, val); return; }
      if (type == 'audio-delay') { _audioDelay = val; _applyDelay(type, val); return; }
      _applyPropertiesToPlayer();
    });
  }

  @override
  Widget build(BuildContext context) {
    String title = 'Điều chỉnh';
    if (widget.mode == SidePanelMode.color) title = 'Màu sắc Video';
    if (widget.mode == SidePanelMode.subtitle) title = 'Đồng bộ Phụ đề';
    if (widget.mode == SidePanelMode.audio) title = 'Đồng bộ Âm thanh';

    return Container(
      width: 350,
      height: double.infinity,
      color: Colors.black.withOpacity(0.85),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: const BoxDecoration(
              border: Border(bottom: BorderSide(color: Colors.white24, width: 1)),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(title, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                IconButton(icon: const Icon(Icons.close, color: Colors.white), onPressed: widget.onClose),
              ],
            ),
          ),
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (widget.mode == SidePanelMode.color) ...[
                    const Text('Bộ lọc:', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
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
                    const SizedBox(height: 24),
                    _buildSlider('Độ sáng', _brightness, -100, 100, (v) => _onSliderChanged('brightness', v)),
                    _buildSlider('Tương phản', _contrast, -100, 100, (v) => _onSliderChanged('contrast', v)),
                    _buildSlider('Độ bão hòa màu', _saturation, -100, 100, (v) => _onSliderChanged('saturation', v)),
                  ],
                  if (widget.mode == SidePanelMode.subtitle) ...[
                    const Text('Chỉnh độ trễ hiển thị phụ đề so với video. Số âm (-) nghĩa là phụ đề hiện sớm hơn.', style: TextStyle(color: Colors.white70, fontSize: 13)),
                    const SizedBox(height: 16),
                    _buildSlider('Độ trễ (ms)', _subDelay, -5000, 5000, (v) => _onSliderChanged('sub-delay', v), isMs: true),
                    const SizedBox(height: 8),
                    Center(
                      child: TextButton.icon(
                        icon: const Icon(Icons.restore),
                        label: const Text('Mặc định (0 ms)'),
                        onPressed: () => _onSliderChanged('sub-delay', 0),
                      ),
                    ),
                  ],
                  if (widget.mode == SidePanelMode.audio) ...[
                    const Text('Chỉnh độ trễ âm thanh so với video. Số âm (-) nghĩa là âm thanh phát sớm hơn.', style: TextStyle(color: Colors.white70, fontSize: 13)),
                    const SizedBox(height: 16),
                    _buildSlider('Độ trễ (ms)', _audioDelay, -5000, 5000, (v) => _onSliderChanged('audio-delay', v), isMs: true),
                    const SizedBox(height: 8),
                    Center(
                      child: TextButton.icon(
                        icon: const Icon(Icons.restore),
                        label: const Text('Mặc định (0 ms)'),
                        onPressed: () => _onSliderChanged('audio-delay', 0),
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSlider(String label, double value, double min, double max, Function(double) onChanged, {bool isMs = false}) {
    String valStr = isMs ? ' ms' : '';
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: const TextStyle(color: Colors.white70, fontSize: 13)),
            Text(valStr, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold)),
          ],
        ),
        Slider(
          value: value,
          min: min,
          max: max,
          divisions: isMs ? (max - min) ~/ 100 : (max - min).toInt(),
          activeColor: Colors.blueAccent,
          inactiveColor: Colors.white24,
          onChanged: onChanged,
        ),
        const SizedBox(height: 16),
      ],
    );
  }
}
