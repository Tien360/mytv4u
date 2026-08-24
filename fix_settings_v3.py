with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

ambient_start = content.find("SwitchListTile(\n                                            title: const Text('Ambient Background')")
if ambient_start == -1:
    ambient_start = content.find("SwitchListTile(\n                                          title: const Text('Ambient Background')")

# let's just find "const Text('Ambient Background')"
import re
match = re.search(r"(\s*SwitchListTile\(\s*title: const Text\('Ambient Background'\)[\s\S]*?\}\s*,\s*\)\s*,\s*const Divider\(color: Colors\.white12\),)", content)

if match:
    ambient_block = match.group(1)
    content = content.replace(ambient_block, "")
    
    lang_regex = r"(\s*const SizedBox\(height: 48\),\s*SizedBox\(key: _languageKey\),)"
    lm = re.search(lang_regex, content)
    
    replacement = """
                                    GlassContainer(
                                      padding: const EdgeInsets.all(16),
                                      child: """ + ambient_block.replace("const Divider(color: Colors.white12),", "").strip() + """
                                    ),
""" + lm.group(1)
    content = content.replace(lm.group(1), replacement)
    
    with open("lib/screens/settings_screen.dart", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed!")
else:
    print("Not found")
