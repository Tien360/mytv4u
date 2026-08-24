import re

with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

old_logic = """    bool isVideoFile =
        _currentUrl.contains('.m3u8') || _currentUrl.contains('.mp4');"""
new_logic = """    bool isVideoFile =
        _currentUrl.contains('.m3u8') || 
        _currentUrl.contains('.mp4') || 
        _currentUrl.contains('.flv') || 
        _currentUrl.contains('.mkv') || 
        _currentUrl.contains('proxy.php');"""

if old_logic in text:
    text = text.replace(old_logic, new_logic)
    with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Fixed isVideoFile logic")
else:
    print("Could not find old_logic")
