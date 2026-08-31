import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update formatStr to allow all codecs (including AV1 for 4K/8K)
old_format = """      final formatStr = height == 0
          ? 'bestvideo[vcodec!*=av01]+bestaudio/bestvideo+bestaudio/best'
          : 'bestvideo[vcodec!*=av01][height<=$height]+bestaudio/bestvideo[height<=$height]+bestaudio/best';"""

new_format = """      final formatStr = height == 0
          ? 'bestvideo+bestaudio/best'
          : 'bestvideo[height<=$height]+bestaudio/best';"""

content = content.replace(old_format, new_format)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed AV1 restriction")
