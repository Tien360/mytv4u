import re

def patch(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the block where we initialize the controller
    old_block = r"await _controller\.initialize\(\);"
    new_block = r"await _controller.initialize(userDataFolder: profileDir);"
        
    match = re.search(old_block, content, flags=re.MULTILINE)
    if match:
        content = content.replace(match.group(0), new_block)
    else:
        print("Could not find old block in settings_screen")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch('lib/screens/settings_screen.dart')
print("Patched settings_screen.dart")
