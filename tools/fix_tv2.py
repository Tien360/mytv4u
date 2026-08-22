with open('lib/screens/tv_webview_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'error': _error", "'error': _error ?? ''")

with open('lib/screens/tv_webview_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed error map')
