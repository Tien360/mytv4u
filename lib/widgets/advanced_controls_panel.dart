import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'glass_container.dart';

import '../utils/l10n.dart';
enum SidePanelMode { none, color, subtitle, audio, secondarySubtitle }

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
  String _preset = L10n.t('default');
  double _brightness = 0.0;
  double _contrast = 0.0;
  double _saturation = 0.0;
  
  double _subDelay = 0.0;
double _secSubDelay = 0.0;
  double _audioDelay = 0.0;

  final Map<String, Map<String, double>> _presets = {
    L10n.t('default'): {'brightness': 0.0, 'contrast': 0.0, 'saturation': 0.0},
    L10n.t('vivid'): {'brightness': 5.0, 'contrast': 10.0, 'saturation': 25.0},
    L10n.t('cinema'): {'brightness': -5.0, 'contrast': 15.0, 'saturation': 5.0},
    L10n.t('bright'): {'brightness': 20.0, 'contrast': 5.0, 'saturation': 0.0},
    L10n.t('bw'): {'brightness': 0.0, 'contrast': 5.0, 'saturation': -100.0},
    L10n.t('warm'): {'brightness': 0.0, 'contrast': 5.0, 'saturation': 15.0},
    L10n.t('cool'): {'brightness': 5.0, 'contrast': 5.0, 'saturation': -10.0},
    L10n.t('custom'): {},
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
    if (presetName == L10n.t('custom')) return;
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
      if (type == 'brightness') { _brightness = val; _preset = L10n.t('custom'); }
      if (type == 'contrast') { _contrast = val; _preset = L10n.t('custom'); }
      if (type == 'saturation') { _saturation = val; _preset = L10n.t('custom'); }
      if (type == 'sub-delay') { _subDelay = val; _applyDelay(type, val); return; }
      if (type == 'secondary-sub-delay') { _secSubDelay = val; _applyDelay(type, val); return; }
      if (type == 'audio-delay') { _audioDelay = val; _applyDelay(type, val); return; }
      _applyPropertiesToPlayer();
    });
  }

  @override
  Widget build(BuildContext context) {
    String title = L10n.t('adjust');
    if (widget.mode == SidePanelMode.color) title = L10n.t('video_color');
    if (widget.mode == SidePanelMode.subtitle) title = L10n.t('sync_subtitle');
    if (widget.mode == SidePanelMode.secondarySubtitle) title = L10n.t('sync_subtitle');
    if (widget.mode == SidePanelMode.audio) title = L10n.t('sync_audio');

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
                    Text(L10n.t('filter_label'), style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
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
                    _buildSlider(L10n.t('brightness'), _brightness, -100, 100, (v) => _onSliderChanged('brightness', v)),
                    _buildSlider(L10n.t('contrast'), _contrast, -100, 100, (v) => _onSliderChanged('contrast', v)),
                    _buildSlider(L10n.t('saturation'), _saturation, -100, 100, (v) => _onSliderChanged('saturation', v)),
                  ],
                  if (widget.mode == SidePanelMode.subtitle) ...[
                    Text(L10n.t('sub_delay_desc'), style: TextStyle(color: Colors.white70, fontSize: 13)),
                    const SizedBox(height: 16),
                    _buildSlider(L10n.t('delay_ms'), _subDelay, -5000, 5000, (v) => _onSliderChanged('sub-delay', v), isMs: true),
                    const SizedBox(height: 8),
                    Center(
                      child: TextButton.icon(
                        icon: const Icon(Icons.restore),
                        label: Text(L10n.t('default_0ms')),
                        onPressed: () => _onSliderChanged('sub-delay', 0),
                      ),
                    ),
                  ],
                                    if (widget.mode == SidePanelMode.secondarySubtitle) ...[
                    Text(L10n.t('sub_delay_desc') ?? '', style: const TextStyle(color: Colors.white70, fontSize: 13)),
                    const SizedBox(height: 16),
                    _buildSlider(L10n.t('delay_ms') ?? '', _secSubDelay, -5000, 5000, (v) => _onSliderChanged('secondary-sub-delay', v), isMs: true),
                    const SizedBox(height: 8),
                    Center(
                      child: TextButton.icon(
                        icon: const Icon(Icons.restore),
                        label: Text(L10n.t('default_0ms') ?? ''),
                        onPressed: () => _onSliderChanged('secondary-sub-delay', 0),
                      ),
                    ),
                  ],
                  if (widget.mode == SidePanelMode.audio) ...[
                    Text(L10n.t('audio_delay_desc'), style: TextStyle(color: Colors.white70, fontSize: 13)),
                    const SizedBox(height: 16),
                    _buildSlider(L10n.t('delay_ms'), _audioDelay, -5000, 5000, (v) => _onSliderChanged('audio-delay', v), isMs: true),
                    const SizedBox(height: 8),
                    Center(
                      child: TextButton.icon(
                        icon: const Icon(Icons.restore),
                        label: Text(L10n.t('default_0ms')),
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
