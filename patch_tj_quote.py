import re
path = r"T:\Project\Phim\mytv4u_flutter\lib\widgets\tom_jerry_easter_egg.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("'assets/easter/Tom và Jerry/mèo tom don\\\\'t care.gif'", "\"assets/easter/Tom và Jerry/mèo tom don't care.gif\"")
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
