import io
import re

with io.open(r'lib\screens\player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        if (title.contains('vi') || title.contains('lồng tiếng') || title.contains('thuyết minh') || title.contains('vietnamese') || lang.contains('vi')) {
          player.setAudioTrack(track);
          audioSelected = true;
          break;
        }
      }
      if (!audioSelected) {
        final validTracks = tracks.audio.where((t) => t.id != 'auto' && t.id != 'no').toList();
        if (validTracks.isNotEmpty) {
          player.setAudioTrack(validTracks.first);
        }
      }'''

replacement = '''        if (title.contains('vi') || title.contains('lồng tiếng') || title.contains('thuyết minh') || title.contains('vietnamese') || lang.contains('vi')) {
          _selectedAudioTrack = track;
          player.setAudioTrack(track);
          audioSelected = true;
          break;
        }
      }
      if (!audioSelected) {
        final validTracks = tracks.audio.where((t) => t.id != 'auto' && t.id != 'no').toList();
        if (validTracks.isNotEmpty) {
          _selectedAudioTrack = validTracks.first;
          player.setAudioTrack(validTracks.first);
        }
      }'''
text = text.replace(target, replacement)

target2 = '''        if (title.contains('vi') || title.contains('vietnamese') || lang.contains('vi')) {
          player.setSubtitleTrack(track);
          subSelected = true;
          break;
        }
      }
      if (!subSelected) {
        final validTracks = tracks.subtitle.where((t) => t.id != 'auto' && t.id != 'no').toList();
        if (validTracks.isNotEmpty) {
          player.setSubtitleTrack(validTracks.first);
        }
      }'''
replacement2 = '''        if (title.contains('vi') || title.contains('vietnamese') || lang.contains('vi')) {
          _selectedSubtitleTrack = track;
          player.setSubtitleTrack(track);
          subSelected = true;
          break;
        }
      }
      if (!subSelected) {
        final validTracks = tracks.subtitle.where((t) => t.id != 'auto' && t.id != 'no').toList();
        if (validTracks.isNotEmpty) {
          _selectedSubtitleTrack = validTracks.first;
          player.setSubtitleTrack(validTracks.first);
        }
      }'''
text = text.replace(target2, replacement2)

with io.open(r'lib\screens\player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated player_screen.dart")
