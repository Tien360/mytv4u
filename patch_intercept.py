import re

for file in ["lib/screens/player_screen.dart", "lib/screens/yt_player_screen.dart"]:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the block where rawId is extracted
    old_block = """        if (_currentUrl.startsWith('premium://')) {
            rawId = _currentUrl.replaceFirst('premium://', '');
        } else {
            final uri = Uri.tryParse(_currentUrl); if (uri == null) return; rawId = uri.pathSegments.last;
        }"""
    new_block = """        final uri = Uri.tryParse(_currentUrl); if (uri == null) return; rawId = uri.pathSegments.last;"""
    
    content = content.replace(old_block, new_block)
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

print("Fixed intercept logic")
