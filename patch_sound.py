import re

path = r"T:\Project\Phim\mytv4u_flutter\lib\widgets\minion_easter_egg.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"await _player\.open\(Media\('asset://assets/easter/sfx/swoosh\.wav'\), play: true\);"
repl = """String soundFile = 'minion_laugh.mp3';
      if (widget.effectType == 3 || widget.effectType == 9) {
        soundFile = 'minion_what.mp3';
      }
      await _player.open(Media('asset://assets/easter/sfx/$soundFile'), play: true);"""

content = re.sub(pattern, repl, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated sound in minion_easter_egg.dart")
