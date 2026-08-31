import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

search = """    try {
      await _controller.initialize(userDataFolder: profileDir);
      await _controller.setBackgroundColor(Colors.transparent);"""

new_code = """    try {
      try {
        await WebviewController.initializeEnvironment(userDataPath: profileDir);
      } catch (e) {
        print('Environment already initialized: $e');
      }
      await _controller.initialize();
      await _controller.setBackgroundColor(Colors.transparent);"""

content = content.replace(search, new_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
