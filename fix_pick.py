import os
import re

content = open('lib/screens/library_screen.dart', 'r', encoding='utf-8').read()
content = content.replace('pickResult.files', 'pickResult')
open('lib/screens/library_screen.dart', 'w', encoding='utf-8').write(content)
