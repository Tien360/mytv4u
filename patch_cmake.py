path = r"T:\Project\Phim\mytv4u_flutter\windows\CMakeLists.txt"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('set(BINARY_NAME "mytv4u_flutter")', 'set(BINARY_NAME "MyTV4U")')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced mytv4u_flutter with MyTV4U in CMakeLists.txt")
