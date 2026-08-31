import re

path = r"T:\Project\Phim\tv_web_player\MainForm.cs"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r"ccBtn\.innerHTML = 'CC \(T.*?\)'", r"ccBtn.innerHTML = 'CC (T\\u1EAFt)'", content)
content = re.sub(r"offBtn\.innerHTML = '.*?'", r"offBtn.innerHTML = 'T\\u1EAFt Ph\\u1EE5 \\u0111\\u1EC1'", content)
content = re.sub(r"titleDiv\.innerHTML = '.*?'", r"titleDiv.innerHTML = '<b>Ch\\u1ECDn Ph\\u1EE5 \\u0111\\u1EC1</b>'", content)
content = re.sub(r"track\.lang === 'vie' \? '.*?' :", r"track.lang === 'vie' ? 'Ti\\u1EBFng Vi\\u1EC7t' :", content)
content = re.sub(r"ccBtn\.innerHTML = '\?ang ti\.\.\.'", r"ccBtn.innerHTML = '\\u0110ang t\\u1EA3i...'", content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done patching font issues in MainForm.cs with Python")
