path = r"T:\Project\Phim\mytv4u_flutter\lib\services\deep_link_service.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("// await Process.run('cmd', ['/c', 'ie4uinit.exe', '-show']);", "await Process.run('cmd', ['/c', 'ie4uinit.exe', '-show']);")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Uncommented ie4uinit.exe")
