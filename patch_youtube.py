import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\youtube_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Background transparency
pattern_init = r"await _controller\.initialize\(\);"
repl_init = "await _controller.initialize();\n      await _controller.setBackgroundColor(Colors.transparent);"
content = re.sub(pattern_init, repl_init, content)

# 2. Better JS Injection for Transparency
pattern_css = r"body \{ background-color: transparent !important; \}\s*ytd-app \{ background: transparent !important; \}"
repl_css = """html, body, ytd-app, #background.ytd-app, ytd-page-manager {
          background: transparent !important;
          background-color: transparent !important;
        }"""
content = re.sub(pattern_css, repl_css, content)

# 3. URL intercept in dart
pattern_url_listen = r"_controller\.url\.listen\(\(url\) \{[\s\S]*?\}\);"
repl_url_listen = """_controller.url.listen((url) {
        if (url.contains('/watch?v=') || url.contains('/shorts/')) {
          _controller.goBack();
          _handleYoutubeLink(url);
        }
      });"""
content = re.sub(pattern_url_listen, repl_url_listen, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated youtube_screen")
