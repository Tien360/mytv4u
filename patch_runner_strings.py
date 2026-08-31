path = r"T:\Project\Phim\mytv4u_flutter\windows\runner\Runner.rc"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"mytv4u_flutter"', '"MyTV4U"')
content = content.replace('"mytv4u_flutter.exe"', '"MyTV4U.exe"')
content = content.replace('com.example', 'MyTV4U')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced mytv4u_flutter with MyTV4U in Runner.rc")
