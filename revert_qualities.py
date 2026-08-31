import re

def revert_qualities(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_code = r"Future<void> _fetchYoutubeQualities\(String url\) async \{\s*return; // Disabled because youtube_explode_dart auto-selects best muxed quality"
    new_code = "Future<void> _fetchYoutubeQualities(String url) async {"
    
    content = re.sub(old_code, new_code, content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Reverted _fetchYoutubeQualities!")

revert_qualities('lib/screens/player_screen.dart')
