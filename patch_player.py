import re
with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix _tryFallbackDomain off-by-one
old_fb = '''      _currentFallbackDomainIndex++;

      if (_currentFallbackDomainIndex < _fallbackDomains.length) {
        final newDomain = _fallbackDomains[_currentFallbackDomainIndex];'''
new_fb = '''      if (_currentFallbackDomainIndex < _fallbackDomains.length) {
        final newDomain = _fallbackDomains[_currentFallbackDomainIndex];
        _currentFallbackDomainIndex++;'''

text = text.replace(old_fb, new_fb)

# 2. Fix _isUsingWebview to force NguonC and VSMov
old_webview = '''      _isUsingWebview =
          !isVideoFile &&
          _currentUrl.startsWith('http') &&
          (_currentUrl.contains('embed') ||
              _currentUrl.contains('player') ||
              _currentUrl.contains('iframe') ||
              (ep.m3u8Url.isEmpty && ep.embedUrl.isNotEmpty));'''

new_webview = '''      _isUsingWebview =
          !isVideoFile &&
          _currentUrl.startsWith('http') &&
          (_currentUrl.contains('embed') ||
              _currentUrl.contains('player') ||
              _currentUrl.contains('iframe') ||
              (ep.m3u8Url.isEmpty && ep.embedUrl.isNotEmpty));
              
      if (_currentUrl.contains('nguonc') || _currentUrl.contains('streamc.xyz') || _currentUrl.contains('vsmov')) {
        _isUsingWebview = true;
      }'''

text = text.replace(old_webview, new_webview)

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print('Patched player_screen.dart successfully')
