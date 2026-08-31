content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
content = content.replace("const SizedBox(height: 48);", "const SizedBox(height: 48),")
open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(content)
