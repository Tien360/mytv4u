path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\main_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Th Thao", "Thể Thao")
content = content.replace("Th vin", "Thư viện")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated main_screen.dart encodings")
