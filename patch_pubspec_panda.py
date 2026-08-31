path = r"T:\Project\Phim\mytv4u_flutter\pubspec.yaml"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("    - assets/easter/minions/", "    - assets/easter/minions/\n    - assets/easter/kungfu panda/")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated pubspec.yaml")
