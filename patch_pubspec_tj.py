path = r"T:\Project\Phim\mytv4u_flutter\pubspec.yaml"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "Tom và Jerry" not in content:
    content = content.replace("    - assets/easter/Fast and Furious/", "    - assets/easter/Fast and Furious/\n    - assets/easter/Tom và Jerry/")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated pubspec.yaml")
