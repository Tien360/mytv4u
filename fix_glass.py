import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find the health_utilities section
start_token = "L10n.t('health_utilities'),"
start = content.find(start_token)
if start == -1:
    print("Could not find start token")
    exit(1)

end_token = "const SizedBox(height: 48),"
end = content.find(end_token, start)
if end == -1:
    print("Could not find end token")
    exit(1)

block = content[start:end]

# It looks something like:
# L10n.t('health_utilities'),
# ),
# const SizedBox(height: 16),
# GlassContainer( ... child: ListTile( ... ) ),
# GlassContainer( ... child: SwitchListTile( ... ) ),

# Let's extract the two tiles.
# The first tile is a ListTile for watch limit.
tile1_match = re.search(r"(ListTile\([\s\S]*?\}\s*,\s*\))", block)
if not tile1_match:
    print("Could not find tile 1")
    exit(1)
tile1 = tile1_match.group(1)

# The second tile is a SwitchListTile for Ambient Background.
tile2_match = re.search(r"(SwitchListTile\([\s\S]*?\}\s*,\s*\))", block)
if not tile2_match:
    print("Could not find tile 2")
    exit(1)
tile2 = tile2_match.group(1)

# Replace tile2's texts
tile2 = tile2.replace("const Text('Ambient Background')", "Text(L10n.t('ambient_bg'))")
tile2 = re.sub(r"const Text\(\s*'Hi.*?hon',\s*\)", "Text(L10n.t('ambient_bg_desc'))", tile2, flags=re.DOTALL)

# Reconstruct the section
new_glass = """GlassContainer(
                                    padding: const EdgeInsets.all(16),
                                    child: Column(
                                      children: [
                                        """ + tile1 + """,
                                        const Divider(color: Colors.white12),
                                        """ + tile2 + """,
                                      ],
                                    ),
                                  ),"""

# Now replace everything between `const SizedBox(height: 16),` and `const SizedBox(height: 48),`
before_glass = block[:block.find("GlassContainer")]

new_block = before_glass + new_glass + "\n\n                                  "

content = content[:start] + new_block + content[end:]

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Merged glass containers and localized successfully!")
