path = r"T:\Project\Phim\mytv4u_flutter\pubspec.yaml"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "naruto/" not in content:
    content = content.replace("    - assets/easter/Tom và Jerry/", "    - assets/easter/Tom và Jerry/\n    - assets/easter/naruto/")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated pubspec.yaml")
