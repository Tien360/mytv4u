path = r"T:\Project\Phim\mytv4u_flutter\lib\services\deep_link_service.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\'"$audioIcoPath"\',', '\'"$exePath",1\',')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched deep_link_service.dart with simpler string replace")
