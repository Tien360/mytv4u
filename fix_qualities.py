import re

def fix_qualities(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_code = r"Future<void> _fetchYoutubeQualities\(String url\) async \{"
    new_code = "Future<void> _fetchYoutubeQualities(String url) async {\n      return; // Disabled because youtube_explode_dart auto-selects best muxed quality"
    
    content = re.sub(old_code, new_code, content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_qualities('lib/screens/player_screen.dart')
