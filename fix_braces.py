import re

with open('lib/screens/library_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to add a closing brace for the `build` method.
# `    );`
# `  void _showOpenUrlDialog(BuildContext context) {`

content = content.replace(
"""    );
  void _showOpenUrlDialog""", 
"""    );
  }

  void _showOpenUrlDialog"""
)

# And remove the extra brace at the very end
content = re.sub(r'\}\s*\}\s*$', '}\n', content)

with open('lib/screens/library_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed braces")
