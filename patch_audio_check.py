import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """  bool get _isAudioOnly {
    bool hasRealVideo = _videoTracks.any((t) => t.id != 'auto' && t.id != 'no');
    bool hasRealAudio = _audioTracks.any((t) => t.id != 'auto' && t.id != 'no');
    return hasRealAudio && !hasRealVideo;
  }"""

new_code = """  bool get _isAudioOnly {
    if (widget.episodes.isEmpty) return false;
    final ep = widget.episodes[widget.currentEpisodeIndex];
    
    final url = ep.m3u8Url.toLowerCase();
    final file = (ep.filename ?? '').toLowerCase();
    final name = ep.name.toLowerCase();
    final movName = widget.movieName.toLowerCase();
    
    bool isAudioExt = url.endsWith('.mp3') || url.endsWith('.m4a') || url.endsWith('.flac') || url.endsWith('.wav') ||
                      file.endsWith('.mp3') || file.endsWith('.m4a') || file.endsWith('.flac') || file.endsWith('.wav') ||
                      name.endsWith('.mp3') || name.endsWith('.m4a') || name.endsWith('.flac') || name.endsWith('.wav') ||
                      movName.endsWith('.mp3') || movName.endsWith('.m4a') || movName.endsWith('.flac') || movName.endsWith('.wav');
                      
    if (isAudioExt) return true;

    // Fallback: If there are no video tracks found (or only dummy auto/no tracks)
    // and width is null/0 while playing/loaded, it's audio.
    bool hasRealVideo = _videoTracks.any((t) => t.id != 'auto' && t.id != 'no');
    if (!hasRealVideo && player.state.duration.inSeconds > 0 && (player.state.width == null || player.state.width == 0)) {
      return true;
    }
    
    return false;
  }"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched _isAudioOnly successfully!")
else:
    print("Could not find old _isAudioOnly code to replace!")
