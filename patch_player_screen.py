import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add _sidePanelMode
content = content.replace('bool _showServersPanel = false;', 'bool _showServersPanel = false;\n  SidePanelMode _sidePanelMode = SidePanelMode.none;')

# 2. Add side panel to Stack
side_panel = '''
              // Side Control Panel
              if (_sidePanelMode != SidePanelMode.none)
                Positioned(
                  top: 0,
                  bottom: 0,
                  right: 0,
                  child: SideControlPanel(
                    player: player,
                    mode: _sidePanelMode,
                    onClose: () => setState(() => _sidePanelMode = SidePanelMode.none),
                  ),
                ),
'''
content = content.replace('// Quick Controls Overlay', side_panel + '\n              // Quick Controls Overlay')

# 3. Modify _showSettingsDialog to change length from 6 to 5
content = content.replace('length: 6,', 'length: 5,')
content = content.replace("Tab(text: 'Bộ lọc & Đồng bộ'),", "")
content = content.replace("AdvancedControlsTab(player: player),", "")

# 4. Inject buttons into tabs
btn_color = '''                            ListTile(
                              leading: const Icon(Icons.color_lens, color: Colors.white),
                              title: const Text('Chỉnh màu Video', style: TextStyle(color: Colors.white)),
                              trailing: const Icon(Icons.arrow_forward_ios, color: Colors.white54, size: 16),
                              onTap: () {
                                Navigator.pop(context);
                                setState(() => _sidePanelMode = SidePanelMode.color);
                              },
                            ),'''
content = content.replace("ListTile(\n                              leading: const Icon(Icons.speed, color: Colors.white),", btn_color + "\n                            ListTile(\n                              leading: const Icon(Icons.speed, color: Colors.white),")

btn_audio = '''                            ListTile(
                              leading: const Icon(Icons.av_timer, color: Colors.white),
                              title: const Text('Đồng bộ Âm thanh', style: TextStyle(color: Colors.white)),
                              trailing: const Icon(Icons.arrow_forward_ios, color: Colors.white54, size: 16),
                              onTap: () {
                                Navigator.pop(context);
                                setState(() => _sidePanelMode = SidePanelMode.audio);
                              },
                            ),'''
content = content.replace("const Divider(color: Colors.white24),", btn_audio + "\n                            const Divider(color: Colors.white24),", 1) # Only first divider which is in Audio

btn_sub = '''                            const Divider(color: Colors.white24),
                            ListTile(
                              leading: const Icon(Icons.av_timer, color: Colors.white),
                              title: const Text('Đồng bộ Phụ đề', style: TextStyle(color: Colors.white)),
                              trailing: const Icon(Icons.arrow_forward_ios, color: Colors.white54, size: 16),
                              onTap: () {
                                Navigator.pop(context);
                                setState(() => _sidePanelMode = SidePanelMode.subtitle);
                              },
                            ),'''
# Phụ đề chính tab
content = content.replace('''                              ),
                            ),
                            const Divider(color: Colors.white24),
                            ListTile(
                              leading: const Icon(Icons.file_upload, color: Colors.white),
                              title: Text(L10n.t('sub_load_local'), style: const TextStyle(color: Colors.white)),''', '''                              ),
                            ),''' + btn_sub + '''\n                            const Divider(color: Colors.white24),
                            ListTile(
                              leading: const Icon(Icons.file_upload, color: Colors.white),
                              title: Text(L10n.t('sub_load_local'), style: const TextStyle(color: Colors.white)),''')

# Phụ đề phụ tab
content = content.replace('''                              ),
                            ),
                            const Divider(color: Colors.white24),
                            ListTile(
                              leading: const Icon(Icons.file_upload, color: Colors.white),
                              title: Text(L10n.t('sub_load_local_sec'), style: const TextStyle(color: Colors.white)),''', '''                              ),
                            ),''' + btn_sub + '''\n                            const Divider(color: Colors.white24),
                            ListTile(
                              leading: const Icon(Icons.file_upload, color: Colors.white),
                              title: Text(L10n.t('sub_load_local_sec'), style: const TextStyle(color: Colors.white)),''')


with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched player_screen.dart')
