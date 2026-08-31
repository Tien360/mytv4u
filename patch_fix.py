path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("bool _isLoggingIn = false;", "bool _isLoggingIn = false;\n  bool _isYtLinked = false;")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added _isYtLinked state")
