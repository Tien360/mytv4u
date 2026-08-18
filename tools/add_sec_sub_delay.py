import os
import re

filepath = 'lib/widgets/advanced_controls_panel.dart'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update enum
text = text.replace('enum SidePanelMode { none, color, subtitle, audio }', 'enum SidePanelMode { none, color, subtitle, audio, secondarySubtitle }')

# 2. Add state variable
text = text.replace('  double _subDelay = 0;', '  double _subDelay = 0;\n  double _secSubDelay = 0;')

# 3. Add to _onSliderChanged
text = text.replace("if (type == 'audio-delay')", "if (type == 'secondary-sub-delay') { _secSubDelay = val; _applyDelay(type, val); return; }\n      if (type == 'audio-delay')")

# 4. Add title
text = text.replace("if (widget.mode == SidePanelMode.subtitle) title = L10n.t('sync_subtitle');", "if (widget.mode == SidePanelMode.subtitle) title = L10n.t('sync_subtitle');\n    if (widget.mode == SidePanelMode.secondarySubtitle) title = L10n.t('sync_subtitle');")

# 5. Add UI section
new_ui = '''                  if (widget.mode == SidePanelMode.secondarySubtitle) ...[
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
                  ],'''

text = text.replace("if (widget.mode == SidePanelMode.audio) ...[", new_ui + "\n                  if (widget.mode == SidePanelMode.audio) ...[")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

