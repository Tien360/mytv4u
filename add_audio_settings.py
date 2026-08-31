import os

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

if "final _audioKey =" not in content:
    content = content.replace("final _subtitleKey = GlobalKey();", "final _subtitleKey = GlobalKey();\n  final _audioKey = GlobalKey();")
    
    sidebar_item = '''        _buildSidebarItem(
          L10n.t('subtitles') ?? 'Phụ đề',
          Icons.subtitles,
          _subtitleKey,
        ),
        _buildSidebarItem(
          L10n.t('audio_player_title') ?? 'Trình phát Nhạc',
          Icons.library_music,
          _audioKey,
        ),'''
    content = content.replace('''        _buildSidebarItem(
          L10n.t('subtitles') ?? 'Phụ đề',
          Icons.subtitles,
          _subtitleKey,
        ),''', sidebar_item)

    audio_panel = '''                          _buildSectionHeader(_subtitleKey, L10n.t('subtitles') ?? 'Phụ đề', Icons.subtitles),
                          _buildSubtitleSettings(),
                          
                          _buildSectionHeader(_audioKey, L10n.t('audio_player_title') ?? 'Trình phát Nhạc', Icons.library_music),
                          _buildAudioSettings(),
'''
    content = content.replace('''                          _buildSectionHeader(_subtitleKey, L10n.t('subtitles') ?? 'Phụ đề', Icons.subtitles),
                          _buildSubtitleSettings(),''', audio_panel)
                          
    audio_widget = '''  Widget _buildAudioSettings() {
    return _buildCard([
      ListTile(
        title: const Text('Hiệu ứng sóng âm', style: TextStyle(color: Colors.white)),
        subtitle: const Text('Chọn kiểu hiển thị sóng âm', style: TextStyle(color: Colors.white54)),
        trailing: DropdownButton<String>(
          dropdownColor: Colors.grey[900],
          value: prefs.getString('audio_visualizer') ?? 'bars',
          items: const [
            DropdownMenuItem(value: 'bars', child: Text('Cột sóng', style: TextStyle(color: Colors.white))),
            DropdownMenuItem(value: 'waves', child: Text('Lượn sóng', style: TextStyle(color: Colors.white))),
          ],
          onChanged: (val) {
            if (val != null) {
              prefs.setString('audio_visualizer', val);
              setState(() {});
            }
          },
        ),
      ),
      ListTile(
        title: const Text('Hẹn giờ tắt (phút)', style: TextStyle(color: Colors.white)),
        subtitle: const Text('0 để tắt hẹn giờ', style: TextStyle(color: Colors.white54)),
        trailing: DropdownButton<int>(
          dropdownColor: Colors.grey[900],
          value: prefs.getInt('audio_sleep_timer') ?? 0,
          items: const [
            DropdownMenuItem(value: 0, child: Text('Tắt', style: TextStyle(color: Colors.white))),
            DropdownMenuItem(value: 15, child: Text('15 phút', style: TextStyle(color: Colors.white))),
            DropdownMenuItem(value: 30, child: Text('30 phút', style: TextStyle(color: Colors.white))),
            DropdownMenuItem(value: 60, child: Text('60 phút', style: TextStyle(color: Colors.white))),
          ],
          onChanged: (val) {
            if (val != null) {
              prefs.setInt('audio_sleep_timer', val);
              setState(() {});
            }
          },
        ),
      ),
    ]);
  }

  Widget _buildSubtitleSettings() {'''
    content = content.replace("  Widget _buildSubtitleSettings() {", audio_widget)
    
    open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
    print("Added audio settings to SettingsScreen")
else:
    print("Already added")
