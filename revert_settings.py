import re

def revert_patch(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Revert settings_screen.dart
    old_block = r"await _controller.initialize\(userDataFolder: profileDir\);"
    new_block = r"await _controller.initialize();"
        
    match = re.search(old_block, content, flags=re.MULTILINE)
    if match:
        content = content.replace(match.group(0), new_block)
    else:
        print("Could not find old block in settings_screen")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

revert_patch('lib/screens/settings_screen.dart')
print("Reverted settings_screen.dart")
