import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('lib/screens/movie_detail_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """    final ytKey = await PhimApi.getTrailerStreamUrl(_movie!, isTv);

    if (ytKey != null && mounted) {"""

new_logic = """    final ytKey = await PhimApi.getTrailerStreamUrl(_movie!, isTv);

    if (_userPausedTrailer) return; // FIX: Abort if user paused while loading
    if (ytKey != null && mounted) {"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open('lib/screens/movie_detail_screen.dart', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed _startInlineTrailer")
else:
    print("Could not find old_logic")
