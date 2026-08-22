import re

with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix _isLiveStream getter
old_is_live_getter = r'''  bool get _isLiveStream \{
    if \(widget\.isLive\) return true;
    if \(_autoDetectedLive\) return true;
    
    final currentEp = widget\.episodes\[_currentIndex\];
    final url = currentEp\.m3u8Url\.toLowerCase\(\);
    
    // Auto-detect by URL keywords common in TV / live streams
    if \(url\.contains\('live'\) \|\| 
        url\.contains\('tv360'\) \|\| 
        url\.contains\('channel'\) \|\|
        url\.contains\('stream'\)\) \{
        // Exclude some edge cases if needed, but 'live' usually means livestream
        return true;
    \}
    
    // Auto-detect by MediaKit duration:
    // If playing, position is advancing, but duration stays 0 or very large
    if \(_duration\.inSeconds == 0 && _position\.inSeconds > 0\) return true;
    if \(_duration\.inHours > 24\) return true; // Unlikely to be a real VOD
    
    return false;
  \}'''

new_is_live_getter = r'''  bool get _isLiveStream {
    if (widget.isLive) return true;
    if (_autoDetectedLive) return true;
    
    final currentEp = widget.episodes[_currentIndex];
    final url = currentEp.m3u8Url.toLowerCase();
    
    // Auto-detect by Domain keywords
    try {
      final uri = Uri.parse(url);
      final host = uri.host;
      if (host.contains('live') || host.contains('tv360') || host.contains('vtv')) {
        return true;
      }
    } catch (_) {}
    
    // Auto-detect by MediaKit duration:
    if (_duration.inSeconds == 0 && _position.inSeconds > 0) return true;
    if (_duration.inHours > 24) return true;
    
    return false;
  }'''

content = re.sub(old_is_live_getter, new_is_live_getter, content)

# 2. Fix `isNearEnd` logic in player.stream.completed
old_is_near_end = r'''          final isNearEnd = !_isLiveStream &&
              _duration\.inSeconds > 0 &&
              \(_position\.inSeconds >= _duration\.inSeconds - 120\);'''
              
new_is_near_end = r'''          final isNearEnd =
              _duration.inSeconds > 0 &&
              (_position.inSeconds >= _duration.inSeconds - 120);'''
              
content = re.sub(old_is_near_end, new_is_near_end, content)

# 3. Remove the aggressive sliding window detection that breaks short trailers
old_duration_listener = r'''            // Detect livestreams where duration keeps expanding \(event streams\)
            if \(_duration != Duration\.zero && dur > _duration && \(dur\.inSeconds - _duration\.inSeconds\)\.abs\(\) > 2\) \{
              _autoDetectedLive = true;
            \}
            // Sliding window: duration is small and position is close, and it resets or stays small
            if \(dur\.inSeconds > 0 && dur\.inSeconds < 60 && _position\.inSeconds > 0\) \{
              _autoDetectedLive = true;
            \}'''

new_duration_listener = r'''            // Detect livestreams where duration keeps expanding (event streams)
            if (_duration != Duration.zero && dur > _duration && (dur.inSeconds - _duration.inSeconds).abs() > 5) {
              _autoDetectedLive = true;
            }'''
content = re.sub(old_duration_listener, new_duration_listener, content)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed player_screen.dart")
