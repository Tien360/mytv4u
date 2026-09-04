import sys

with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    c = f.read()

import re

c = re.sub(
    r'onPressed:\s*\(\)\s*=>\s*setState\(\s*\(\)\s*=>\s*_showEpisodePanel\s*=\s*!_showEpisodePanel,\s*\),',
    r'''onPressed: () => setState(() {
                                                      _showEpisodePanel = !_showEpisodePanel;
                                                      if (_showEpisodePanel) {
                                                        _selectedEpisodeChunk = _currentIndex ~/ 50;
                                                      }
                                                    }),''',
    c
)

with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed toggle logic to auto jump chunk")
