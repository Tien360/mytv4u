import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\player_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace "child: Video(" inside children array with just "Video("
bad = """                      children: [
                        child: Video("""
good = """                      children: [
                        Video("""

if bad in content:
    content = content.replace(bad, good)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed syntax error!")
else:
    print("Could not find bad string!")
