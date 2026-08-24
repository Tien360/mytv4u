import re

with open("lib/screens/settings_screen.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Try finding the Ambient block with a more relaxed regex
ambient_regex = r"(\s*SwitchListTile\(\s*title: const Text\('Ambient Background'\),\s*subtitle: const Text\([\s\S]*?\}\),\s*\),\s*const Divider\(color: Colors\.white12\),)"
m = re.search(ambient_regex, content)
if m:
    ambient_block = m.group(1)
    # Remove it
    content = content.replace(ambient_block, "")
    
    # Now find the watch_limit
    watch_limit_regex = r"(child: Text\([\s\S]*?180 \$\{L10n.t\('limit_minutes'\)\}',\s*\),\s*\),\s*],\s*onChanged: \(val\) async \{[\s\S]*?\}\s*,\s*\)\s*,\s*\)\s*,)"
    
    wm = re.search(watch_limit_regex, content)
    if wm:
        watch_block = wm.group(1)
        
        # We want to insert the ambient block after the GlassContainer that contains watch limit.
        # It's better to just put it in a new GlassContainer or inside the column.
        # Actually, let's just insert it right after the GlassContainer of watch limit.
        # Wait, the health section has a GlassContainer.
        # Let's just find `const SizedBox(height: 48),\s*SizedBox(key: _languageKey),`
        
        lang_regex = r"(\s*const SizedBox\(height: 48\),\s*SizedBox\(key: _languageKey\),)"
        lm = re.search(lang_regex, content)
        if lm:
            # insert before this
            replacement = """
                                  GlassContainer(
                                    padding: const EdgeInsets.all(16),
                                    child: """ + ambient_block.strip().replace(",\n                                        const Divider(color: Colors.white12),", ",") + """
                                  ),
""" + lm.group(1)
            content = content.replace(lm.group(1), replacement)
            
            with open("lib/screens/settings_screen.dart", "w", encoding="utf-8") as f2:
                f2.write(content)
            print("Settings modified successfully!")
        else:
            print("Language key not found")
    else:
        print("Watch limit not found")
else:
    print("Ambient block not found")
