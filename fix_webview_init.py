path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("await _controller.initialize(userDataFolder: profileDir);", "await _controller.initialize();")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed userDataFolder parameter")
