import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\screens\settings_screen.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_row = """                                                children: [
                                                  Text('$_skipIntroDuration s', style: const TextStyle(color: Colors.white70)),
                                                  const SizedBox(width: 8),
                                                  Slider("""
new_row = """                                                children: [
                                                  Text('$_skipIntroDuration s', style: const TextStyle(color: Colors.white70)),
                                                  const SizedBox(width: 8),
                                                  Expanded(child: Slider("""
content = content.replace(old_row, new_row)
content = content.replace("                                                  ),", "                                                  )),")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed slider UI")
