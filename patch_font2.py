import re
path = r"T:\Project\Phim\tv_web_player\MainForm.cs"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r"menuTitle\.innerHTML = '.*?'", r"menuTitle.innerHTML = '<b>Ch\\u1ECDn Ph\\u1EE5 \\u0111\\u1EC1</b>'", content)
content = re.sub(r"ccBtn\.innerHTML = '\?ang t.*?'", r"ccBtn.innerHTML = '\\u0110ang t\\u1EA3i...'", content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done patching MainForm.cs again")
