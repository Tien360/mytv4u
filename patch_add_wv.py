import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

search = "DropdownMenuItem(value: 'none', child: Text('Không liên kết (Ẩn danh)')),"
new_code = search + "\n                      DropdownMenuItem(value: 'webview', child: Text('Đăng nhập Trực tiếp trong App (Khuyên dùng)')),"

content = content.replace(search, new_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
