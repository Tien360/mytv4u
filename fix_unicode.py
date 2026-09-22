import io
import re
with io.open(r'lib\screens\player_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()
text = re.sub(r'T\[.*?\]p', r'T[\\u1EA1a\\u1EAD\\u00E2]p', text)
text = re.sub(r'ph\[.*?\]n', r'ph[\\u1EA7a]n', text)
text = re.sub(r'm\[.*?\]a', r'm[\\u00F9u]a', text)
with io.open(r'lib\screens\player_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
