import re

path = r"T:\Project\Phim\tv_web_player\MainForm.cs"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern2 = r"style\.innerHTML = \s*\.jw-ad, \.jw-ad-controls, iframe\[src\*='ads'\], \.ad-container, \.popunder, \[id\*='popad'\], \.ads-banner, \[class\*='-ad-'\] \{\s*display: none !important;\s*opacity: 0 !important;\s*pointer-events: none !important;\s*width: 0 !important;\s*height: 0 !important;\s*\};"

new_css2 = """style.innerHTML = `
                        .jw-ad, .jw-ad-controls, iframe[src*='ads'], .ad-container, .popunder, [id*='popad'], .ads-banner, [class*='-ad-'] {
                            display: none !important;
                            opacity: 0 !important;
                            pointer-events: none !important;
                            width: 0 !important;
                            height: 0 !important;
                        };
                    `;"""

content = re.sub(pattern2, new_css2, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done patching ad CSS syntax error in MainForm.cs")
