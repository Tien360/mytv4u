import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Import
for i, line in enumerate(lines):
    if "import 'package:glassmorphism_ui/glassmorphism_ui.dart';" in line:
        lines.insert(i+1, "import 'package:mytv4u/widgets/advanced_controls_panel.dart';\n")
        break

# 2. State variable
for i, line in enumerate(lines):
    if 'bool _showEpisodePanel = false;' in line:
        lines.insert(i+1, "  bool _showAdvancedPanel = false;\n")
        break

# 3. Button next to Settings
for i, line in enumerate(lines):
    if 'tooltip: \'Cài đặt\',' in line:
        # Find the start of Settings IconButton
        for j in range(i, i-20, -1):
            if '// Settings Gear Button' in lines[j]:
                btn = '''                                            // Advanced Filters Button
                                            IconButton(
                                              icon: const Icon(
                                                Icons.tune,
                                                color: Colors.white,
                                                size: 20,
                                              ),
                                              onPressed: () => setState(() {
                                                _showAdvancedPanel = !_showAdvancedPanel;
                                                _showEpisodePanel = false; // close the other
                                              }),
                                              tooltip: 'Bộ lọc & Đồng bộ',
                                              padding: const EdgeInsets.all(4),
                                              constraints: const BoxConstraints(),
                                            ),
                                            const SizedBox(width: 10),
'''
                lines.insert(j, btn)
                break
        break

# 4. Render Panel
for i, line in enumerate(lines):
    if '// 3. Episode Selection Panel (Right Sidebar)' in line:
        panel = '''                // 4. Advanced Controls Panel
                if (!_isPiPMode)
                  AnimatedPositioned(
                  duration: const Duration(milliseconds: 300),
                  curve: Curves.easeInOut,
                  top: 0,
                  bottom: 0,
                  right: _showAdvancedPanel ? 0 : -350,
                  width: 350,
                  child: AdvancedControlsPanel(
                    player: player,
                    onClose: () => setState(() => _showAdvancedPanel = false),
                  ),
                ),

'''
        lines.insert(i, panel)
        break

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done injecting Advanced Controls!')
