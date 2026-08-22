import re
with open('lib/screens/tv_webview_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r"L10n\.t\('([^']+)'(?:, ([^)]+))?\) \?\? '[^']+'", r"L10n.t('\1'\2)", content)
content = re.sub(r"L10n\.t\('([^']+)'\) \?\? '[^']+'", r"L10n.t('\1')", content)

with open('lib/screens/tv_webview_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed warnings')
