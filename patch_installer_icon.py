path = r"T:\Project\Phim\mytv4u_flutter\installer.iss"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"{app}\\\\audio.ico"', '"{app}\\\\MyTV4U.exe,1"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated installer.iss to use embedded audio icon")
