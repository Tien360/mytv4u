import re

def clean_experimental_flags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("platform.setProperty('vd-lavc-dr', 'yes'); // Direct Rendering", "")
    content = content.replace("platform.setProperty('hwdec', 'auto-copy'); // An toàn cho Optimus", "platform.setProperty('hwdec', 'auto'); // Mặc định an toàn nhất")
    content = content.replace("platform.setProperty('d3d11-exclusive-fs', 'yes');", "")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

clean_experimental_flags('lib/screens/player_screen.dart')
clean_experimental_flags('lib/screens/tv_player_screen.dart')
print("Cleaned up risky flags")
