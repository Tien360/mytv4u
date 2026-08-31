import re
content = open('task.md', 'r', encoding='utf-8').read()
content = content.replace('- [ ] Update settings_screen.dart layout', '- [x] Update settings_screen.dart layout')
content = content.replace('- [ ] Add new language keys', '- [x] Add new language keys')
content = content.replace('- [ ] Update optimizer_dialog.dart', '- [x] Update optimizer_dialog.dart')
content = content.replace('- [ ] Test layout and dialog visually', '- [x] Test layout and dialog visually')
open('task.md', 'w', encoding='utf-8').write(content)
