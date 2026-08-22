import re

with open('lib/screens/library_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# The missing brackets should be right before:
#                 ],
#               ),
#             ),
#             Expanded(

fix = """
                      } catch (e) {
                        print("File picker error: " + e.toString());
                      }
                    },
                  ),
                  ],
                  ),
"""

content = re.sub(r'\}\s*catch\s*\(e\)\s*\{\s*print\("File picker error: "\s*\+\s*e\.toString\(\)\);\s*\}\s*\},?\s*\),?', fix, content)

with open('lib/screens/library_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed syntax")
