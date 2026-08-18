import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the row wrapping _languageKey
bad_pattern = r'\s*Row\(\s*mainAxisAlignment: MainAxisAlignment\.spaceBetween,\s*children: \[\s*SizedBox\(key: _languageKey\),'

text = re.sub(bad_pattern, '\n                          SizedBox(key: _languageKey),', text)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed!')
