
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# We want to replace the boxShadow logic in the poster to always have a shadow.
# Currently:
# boxShadow: [
#   if (_isHovered)
#     BoxShadow(
#       color: Colors.white.withOpacity(0.3), // Glow effect
#       blurRadius: 20,
#       spreadRadius: 2,
#     ),
# ],

new_shadow = '''boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.5),
                blurRadius: 24,
                spreadRadius: 4,
                offset: const Offset(0, 12),
              ),
              if (_isHovered)
                BoxShadow(
                  color: Colors.white.withOpacity(0.2),
                  blurRadius: 20,
                  spreadRadius: 2,
                ),
            ],'''

content = re.sub(r'boxShadow:\s*\[\s*if\s*\(_isHovered\)\s*BoxShadow\([\s\S]*?blurRadius:\s*20,\s*spreadRadius:\s*2,\s*\),\s*\],', new_shadow, content)

with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated poster shadow')

