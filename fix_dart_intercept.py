import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\youtube_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern_dart_url = r"if \(url\.contains\('/watch\?v='\)\s*\|\|\s*url\.contains\('/shorts/'\)\) \{"
repl_dart_url = "if (url.contains('/watch') || url.contains('/shorts/') || url.contains('/live/') || url.contains('/playlist?list=')) {"
content = re.sub(pattern_dart_url, repl_dart_url, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed dart url intercept")
