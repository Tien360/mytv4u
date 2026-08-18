import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Find the start of the buggy Row and replace it
buggy_str = '''                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                SizedBox(key: _languageKey),'''

fixed_str = '''                            SizedBox(key: _languageKey),'''

text = text.replace(buggy_str, fixed_str)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print('Done')
