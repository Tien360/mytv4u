import re

content = open('lib/screens/audio_player_screen.dart', 'r', encoding='utf-8').read()

old_add = '''  Future<void> _addFiles(Function setSheetState) async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['mp3', 'wav', 'flac', 'm4a', 'aac', 'wma', 'ogg'],
      allowMultiple: true,
    );
    if (result != null && result.files.isNotEmpty) {
      setState(() {
        for (var file in result.files) {
          if (file.path != null) {
            _playlistFiles.add(file);
          }
        }
      });
      setSheetState(() {});
    }
  }'''

new_add = '''  Future<void> _addFiles(Function setSheetState) async {
    var files = await FilePicker.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['mp3', 'wav', 'flac', 'm4a', 'aac', 'wma', 'ogg'],
      allowMultiple: true,
    );
    if (files != null && files.isNotEmpty) {
      setState(() {
        for (var file in files) {
          if (file.path != null) {
            _playlistFiles.add(file);
          }
        }
      });
      setSheetState(() {});
    }
  }'''

content = content.replace(old_add, new_add)
open('lib/screens/audio_player_screen.dart', 'w', encoding='utf-8').write(content)
