import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()
start_idx = content.find("SizedBox(key: _accountKey),")
info_end = content.find("const SizedBox(height: 120),", start_idx)

full_content = content[start_idx:info_end]
blocks = re.split(r'\s*const SizedBox\(height: 48\),\s*', full_content)

for i, b in enumerate(blocks):
    keys = re.findall(r'SizedBox\(key: _[a-zA-Z]+Key\)', b)
    print(f"Block {i}: {keys}")
