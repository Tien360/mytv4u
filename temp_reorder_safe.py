import re
content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

start_marker = "SizedBox(key: _accountKey),"
end_marker = "                                  const SizedBox("
start_idx = content.find(start_marker)
# Find the end of the settings list, which is const SizedBox(height: 64) 
end_idx = content.find("                                  const SizedBox(\n                                    height: 64,\n                                  )", start_idx)

full_content = content[start_idx:end_idx]

# Split by const SizedBox(height: 48),
blocks = re.split(r'\s*const SizedBox\(height:\s*48\),?\s*', full_content)

parsed_blocks = {}
for b in blocks:
    if not b.strip(): continue
    # find which key this block belongs to
    keys = re.findall(r'SizedBox\(key: _([a-zA-Z]+)Key\)', b)
    if keys:
        k = keys[0]
        # Wait, does any block have MULTIPLE keys?
        if len(keys) > 1:
            print(f"Warning: Block has multiple keys! {keys}")
        parsed_blocks['_' + k + 'Key'] = b.strip()

print(f"Extracted keys: {list(parsed_blocks.keys())}")

order = [
    '_accountKey',
    '_systemKey',
    '_languageKey',
    '_sourcesKey',
    '_videoKey',
    '_audioKey',
    '_colorKey',
    '_subtitleKey',
    '_shortcutsKey',
    '_infoKey'
]

assembled = ""
for k in order:
    if k in parsed_blocks:
        assembled += "                                  " + parsed_blocks[k] + ",\n                                  const SizedBox(height: 48),\n"

# Remove the last SizedBox
assembled = assembled.rsplit("                                  const SizedBox(height: 48),\n", 1)[0]

# Now replace the original content
final_content = content[:start_idx] + assembled + "\n" + content[end_idx:]

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(final_content)
print("Done reordering!")
