import io
import re

with io.open(r'lib\screens\player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Hide 'auto' track from lists
pattern_tracks = r"setState\(\(\) \{\s*_videoTracks = tracks.video;\s*_audioTracks = tracks.audio;\s*_subtitleTracks = tracks.subtitle;"
replacement_tracks = '''setState(() {
            _videoTracks = tracks.video;
            _audioTracks = tracks.audio.where((t) => t.id != 'auto').toList();
            _subtitleTracks = tracks.subtitle.where((t) => t.id != 'auto').toList();'''
text = re.sub(pattern_tracks, replacement_tracks, text, flags=re.MULTILINE)

# 2. Update _autoSelectVietnameseTracks
target = '''  void _autoSelectVietnameseTracks(Tracks tracks) {
    if (_hasAutoSelectedTracks) return;
    
    // Auto-select Vietnamese Audio
    if (_selectedAudioTrack?.id == 'auto' || _selectedAudioTrack == null) {
      for (var track in tracks.audio) {
        final title = track.title?.toLowerCase() ?? '';
        final lang = track.language?.toLowerCase() ?? '';
        if (title.contains('vi') || title.contains('lồng tiếng') || title.contains('thuyết minh') || title.contains('vietnamese') || lang.contains('vi')) {
          player.setAudioTrack(track);
          break;
        }
      }
    }

    // Auto-select Vietnamese Subtitle
    if (_selectedSubtitleTrack?.id == 'auto' || _selectedSubtitleTrack == null) {
      for (var track in tracks.subtitle) {
        final title = track.title?.toLowerCase() ?? '';
        final lang = track.language?.toLowerCase() ?? '';
        if (title.contains('vi') || title.contains('vietnamese') || lang.contains('vi')) {
          player.setSubtitleTrack(track);
          break;
        }
      }
    }
    
    _hasAutoSelectedTracks = true;
  }'''

replacement_auto = '''  void _autoSelectVietnameseTracks(Tracks tracks) {
    if (_hasAutoSelectedTracks) return;
    
    // Auto-select Vietnamese Audio
    if (_selectedAudioTrack?.id == 'auto' || _selectedAudioTrack == null) {
      bool audioSelected = false;
      for (var track in tracks.audio) {
        final title = track.title?.toLowerCase() ?? '';
        final lang = track.language?.toLowerCase() ?? '';
        if (title.contains('vi') || title.contains('lồng tiếng') || title.contains('thuyết minh') || title.contains('vietnamese') || lang.contains('vi')) {
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
      }
    }

    // Auto-select Vietnamese Subtitle
    if (_selectedSubtitleTrack?.id == 'auto' || _selectedSubtitleTrack == null) {
      bool subSelected = false;
      for (var track in tracks.subtitle) {
        final title = track.title?.toLowerCase() ?? '';
        final lang = track.language?.toLowerCase() ?? '';
        if (title.contains('vi') || title.contains('vietnamese') || lang.contains('vi')) {
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
      }
    }
    
    _hasAutoSelectedTracks = true;
  }'''

text = text.replace(target, replacement_auto)

with io.open(r'lib\screens\player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated player_screen.dart")
