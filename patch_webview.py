import re
with open('lib/screens/player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r"_isUsingWebview =\s*!isVideoFile &&\s*_currentUrl\.startsWith\('http'\) &&\s*\(_currentUrl\.contains\('embed'\) \|\|\s*_currentUrl\.contains\('player'\) \|\|\s*_currentUrl\.contains\('iframe'\) \|\|\s*\(ep\.m3u8Url\.isEmpty && ep\.embedUrl\.isNotEmpty\)\);"

new_webview = '''_isUsingWebview =
        !isVideoFile &&
        _currentUrl.startsWith('http') &&
        (_currentUrl.contains('embed') ||
            _currentUrl.contains('player') ||
            _currentUrl.contains('iframe') ||
            (ep.m3u8Url.isEmpty && ep.embedUrl.isNotEmpty));
            
    if (_currentUrl.contains('nguonc') || _currentUrl.contains('streamc.xyz') || _currentUrl.contains('vsmov')) {
      _isUsingWebview = true;
    }'''

text, count = re.subn(pattern, new_webview, text)
print(f'Replaced {count} times')

with open('lib/screens/player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
