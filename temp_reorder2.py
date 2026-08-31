import re

content = open('lib/screens/settings_screen.dart', 'r', encoding='utf-8').read()

keys = ['_accountKey', '_systemKey', '_languageKey', '_sourcesKey', '_videoKey', '_audioKey', '_colorKey', '_subtitleKey', '_shortcutsKey', '_infoKey']

start_anchor = "                                  SizedBox(key: _accountKey),"
end_anchor = "                                  const SizedBox(height: 120),"

start_idx = content.find(start_anchor)
# Actually, _sourcesKey has Row( before it.
# Let's find the start of each block by looking for the widget that contains the key.
# A block starts either at SizedBox(key: ...) or Row( ... SizedBox(key: _sourcesKey)
# We can just split the entire content by regex matching the start of blocks.

# Let's find the character indices for the start of each block.
indices = []
for k in keys:
    if k == '_sourcesKey':
        # Find the Row before it
        key_idx = content.find("SizedBox(key: _sourcesKey)")
        row_idx = content.rfind("Row(", 0, key_idx)
        indices.append((k, row_idx))
    else:
        indices.append((k, content.find(f"SizedBox(key: {k})")))

indices.sort(key=lambda x: x[1])

blocks = {}
for i in range(len(indices)):
    k, start = indices[i]
    if i < len(indices) - 1:
        end = indices[i+1][1]
    else:
        end = content.find("const SizedBox(height: 120),", start)
    
    block_content = content[start:end].strip()
    # Strip any trailing const SizedBox(height: 48), or commas
    block_content = re.sub(r'const SizedBox\(height:\s*48\),?$', '', block_content).strip()
    if block_content.endswith(','):
        block_content = block_content[:-1].strip()
        
    blocks[k] = block_content

print("Extracted blocks:")
for k in keys:
    print(f"{k}: {len(blocks[k])} chars")

# Now reorder them
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
    assembled += "                                  " + blocks[k] + ",\n                                  const SizedBox(height: 48),\n"

# Remove the last SizedBox
assembled = assembled.rsplit("                                  const SizedBox(height: 48),\n", 1)[0]

# Now replace the original content
final_content = content[:indices[0][1]] + assembled + "\n                                  " + content[content.find("const SizedBox(height: 120),", indices[-1][1]):]

open('lib/screens/settings_screen.dart', 'w', encoding='utf-8').write(final_content)
print("Done reordering!")
