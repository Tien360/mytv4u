content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()
start_idx = content.find('  void _showAudioSettings() {')
end_idx = content.find('  Future<Uint8List?> _getCoverForFile')
if start_idx != -1 and end_idx != -1:
    open('settings_temp.dart', 'w', encoding='utf-8').write(content[start_idx:end_idx])
