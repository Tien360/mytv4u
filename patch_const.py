path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("const Text(L10n.t(", "Text(L10n.t(")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed const from Text(L10n.t)")
