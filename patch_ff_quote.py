import re
path = r"T:\Project\Phim\mytv4u_flutter\lib\widgets\fast_furious_easter_egg.dart"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("'assets/easter/Fast and Furious/i don\\\\'t have friend i got family.gif'", "\"assets/easter/Fast and Furious/i don't have friend i got family.gif\"")
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
