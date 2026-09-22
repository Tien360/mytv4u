import re

with open("lib/screens/yt_player_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Replace _tryFallbackDomain
content = content.replace(
"""    if (_currentUrl.contains('dpdns.org') ||
        _currentUrl.contains('workers.dev') ||
        _currentUrl.contains('railway.app')) {""",
"""    if (_currentUrl.contains('dpdns.org') ||
        _currentUrl.contains('workers.dev') ||
        _currentUrl.contains('railway.app') ||
        _currentUrl.startsWith('premium://')) {"""
)

# Replace the check in _initEpisode
old_check = """    if (_currentUrl.contains('workers.dev') || _currentUrl.contains('dpdns.org')) {
        final uri = Uri.tryParse(_currentUrl); if (uri == null) return; final rawId = uri.pathSegments.last;"""

new_check = """    if (_currentUrl.startsWith('premium://') || _currentUrl.contains('workers.dev') || _currentUrl.contains('dpdns.org')) {
        String rawId = '';
        if (_currentUrl.startsWith('premium://')) {
            rawId = _currentUrl.replaceFirst('premium://', '');
        } else {
            final uri = Uri.tryParse(_currentUrl); if (uri == null) return; rawId = uri.pathSegments.last;
        }"""
        
content = content.replace(old_check, new_check)

with open("lib/screens/yt_player_screen.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("yt_player_screen.dart patched")
