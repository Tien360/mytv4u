import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

search = """            if (_bgWebviewController != null && _bgWebviewController!.value.isInitialized)
              Positioned(
                top: -2000,
                left: -2000,
                width: 1280,
                height: 720,
                child: Webview(_bgWebviewController!),
              ),"""
              
new_stack = """            if (_bgWebviewController != null && _bgWebviewController!.value.isInitialized)
              Positioned(
                top: 0,
                left: 0,
                width: 1,
                height: 1,
                child: Opacity(
                  opacity: 0.01,
                  child: IgnorePointer(child: Webview(_bgWebviewController!)),
                ),
              ),"""
content = content.replace(search, new_stack)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Webview position")
