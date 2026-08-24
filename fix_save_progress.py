with open("lib/screens/player_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

old_func = """  Future<void> _saveLocalProgress() async {
    if (_position.inMilliseconds > 0 && _duration.inMilliseconds > 0) {"""
new_func = """  Future<void> _saveLocalProgress() async {
    if (widget.isLive) return; // Do not save progress for live streams
    if (_position.inMilliseconds > 0 && _duration.inMilliseconds > 0) {"""

if old_func in text:
    text = text.replace(old_func, new_func)
    with open("lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
        f.write(text)
    print("Disabled _saveLocalProgress for live streams.")
else:
    print("Function not found.")
