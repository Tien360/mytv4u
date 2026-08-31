import os
content = open('lib/screens/library_screen.dart', 'r', encoding='utf-8').read()
content = content.replace('files.files', 'files')
open('lib/screens/library_screen.dart', 'w', encoding='utf-8').write(content)
