import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove _showAdvancedPanel state
content = content.replace('bool _showAdvancedPanel = false;', '')
content = content.replace('if (_showEpisodePanel) _showAdvancedPanel = false;', '')

# 2. Remove AdvancedControlsPanel from stack
stack_code = '''                // 4. Advanced Controls Panel
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
                ),'''
content = content.replace(stack_code, '')

# 3. Remove Advanced Filters Button
btn_code = '''                                            // Advanced Filters Button
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
                                            const SizedBox(width: 10),'''
content = content.replace(btn_code, '')

# 4. Modify settings dialog tab count and add new tab
content = content.replace('length: 5,', 'length: 6,')

new_tabs = '''                            const Tab(
                              icon: Icon(Icons.info_outline),
                              text: 'Thông tin',
                            ),
                            const Tab(
                              icon: Icon(Icons.tune),
                              text: 'Bộ lọc & Đồng bộ',
                            ),'''
content = content.replace('''                            const Tab(
                              icon: Icon(Icons.info_outline),
                              text: 'Thông tin',
                            ),''', new_tabs)

new_tab_view = '''                                  ],
                                ),
                              ),
                            ),
                            // Tab Bộ lọc & Đồng bộ
                            AdvancedControlsTab(player: player),
                          ],
                        ),'''
content = content.replace('''                                  ],
                                ),
                              ),
                            ),
                          ],
                        ),''', new_tab_view)

# Fix AdvancedControlsPanel class name in import
content = content.replace('AdvancedControlsPanel', 'AdvancedControlsTab')

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched player_screen.dart')
