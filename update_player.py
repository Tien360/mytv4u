import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add _autoDetectedLive state
state_vars = r'''  bool _isUsingWebview = false;
  bool _autoDetectedLive = false;'''
content = re.sub(r'  bool _isUsingWebview = false;', state_vars, content)

# 2. Add a helper getter to check if it's considered live
is_live_getter = r'''
  bool get _isLiveStream {
    if (widget.isLive) return true;
    if (_autoDetectedLive) return true;
    
    final currentEp = widget.episodes[_currentIndex];
    final url = currentEp.m3u8Url.toLowerCase();
    
    // Auto-detect by URL keywords common in TV / live streams
    if (url.contains('live') || 
        url.contains('tv360') || 
        url.contains('channel') ||
        url.contains('stream')) {
        // Exclude some edge cases if needed, but 'live' usually means livestream
        return true;
    }
    
    // Auto-detect by MediaKit duration:
    // If playing, position is advancing, but duration stays 0 or very large
    if (_duration.inSeconds == 0 && _position.inSeconds > 0) return true;
    if (_duration.inHours > 24) return true; // Unlikely to be a real VOD
    
    return false;
  }
'''

content = re.sub(r'(  String\? errorMsg;)', is_live_getter + r'\1', content)

# 3. Update the `isNearEnd` check in stream.completed
# Replace:
#           final isNearEnd =
#               _duration.inSeconds > 0 &&
#               (_position.inSeconds >= _duration.inSeconds - 120);

new_completed_logic = r'''
          final isNearEnd = !_isLiveStream &&
              _duration.inSeconds > 0 &&
              (_position.inSeconds >= _duration.inSeconds - 120);
'''
content = re.sub(r'          final isNearEnd =\s*_duration\.inSeconds > 0 &&\s*\(_position\.inSeconds >= _duration\.inSeconds - 120\);', new_completed_logic, content)

# 4. Update the Next Episode Overlay
# Replace:
#                   if (!widget.isLive &&
#                       _duration.inSeconds > 0 &&
#                       (_duration.inSeconds - _position.inSeconds) <= 30 &&
#                       !_isUsingWebview)

new_overlay_logic = r'''
                  if (!_isLiveStream &&
                      _duration.inSeconds > 0 &&
                      (_duration.inSeconds - _position.inSeconds) <= 30 &&
                      !_isUsingWebview)'''
content = re.sub(r'                  if \(!widget\.isLive &&\s*_duration\.inSeconds > 0 &&\s*\(_duration\.inSeconds - _position\.inSeconds\) <= 30 &&\s*!_isUsingWebview\)', new_overlay_logic, content)

# 5. In player.stream.duration, detect sliding window or expanding duration
# Find:
#     _playerSubs.add(
#       player.stream.duration.listen((dur) {
#         if (mounted) setState(() => _duration = dur);
#       }),
#     );

new_duration_listener = r'''
    _playerSubs.add(
      player.stream.duration.listen((dur) {
        if (mounted) {
          setState(() {
            // Detect livestreams where duration keeps expanding (event streams)
            if (_duration != Duration.zero && dur > _duration && (dur.inSeconds - _duration.inSeconds).abs() > 2) {
              _autoDetectedLive = true;
            }
            // Sliding window: duration is small and position is close, and it resets or stays small
            if (dur.inSeconds > 0 && dur.inSeconds < 60 && _position.inSeconds > 0) {
              _autoDetectedLive = true;
            }
            _duration = dur;
          });
        }
      }),
    );
'''
content = re.sub(r'    _playerSubs\.add\(\s*player\.stream\.duration\.listen\(\(dur\) \{\s*if \(mounted\) setState\(\(\) => _duration = dur\);\s*\}\),\s*\);', new_duration_listener, content)


with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated player_screen.dart")
