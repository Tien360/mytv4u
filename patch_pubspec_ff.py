path = r"T:\Project\Phim\mytv4u_flutter\pubspec.yaml"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if "Fast and Furious" not in content:
    content = content.replace("    - assets/easter/kungfu panda/", "    - assets/easter/kungfu panda/\n    - assets/easter/Fast and Furious/")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated pubspec.yaml")
